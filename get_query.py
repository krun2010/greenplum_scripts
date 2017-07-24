#!/usr/bin/python
from multiprocessing import Pool
import sys
import os
import commands
import Queue
import threading
import time

## Version 1.0
## Create by Alex Jiang 
## Email: ajiang@pivotal.io 

def splitfile(dir):
  cmd = 'split -b 512m ' + dir + ' ' + dir + 'part'
  print "start to split the log file into 510MB small files : ", cmd  
  (status, output) = commands.getstatusoutput(cmd)
  if status:    
    sys.stderr.write(output)
    sys.exit(status)

def fgrep_function(split_file,conNum,cmdNum):
  cmd='fgrep'+ ' ' + conNum +','+ cmdNum +' '+ split_file
# print "command to run:", cmd   ## This will print out which file the child thread is fgreping, we can comment this line if you don't want to know that
  (status, output) = commands.getstatusoutput(cmd)
  return (status,output,split_file)
 
def get_query_from_match_split_file(split_file,conNUM,cmdNUM):
  start_offset=conNUM+','+cmdNUM
  end_offset='[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}'
  sed_cmd="sed -n '/"+start_offset+"/,/"+end_offset+"/p'"+" "+split_file+"> " +conNUM+cmdNUM+".out"
  print "The SQL is in " +conNUM+cmdNUM+".out"
  (status,output) = commands.getstatusoutput(sed_cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)

# in the below part of the script,it will start up two thread
# The first one is the monitor thread result_th()
# The other thread is pool_th() which will start muti-thread processes to do the fgrep
# The pool_th() will die immediately after kicking off fgrep, the result_th() will stay alive and terminate the fgrep process pool if it found the result.

def main():
#  splitfile(sys.argv[1])
  if len(sys.argv) < 3:
      print("This program requires at least 3 parameter")
      print("Example: get_query.py <LOG PATH> <Con Num> <CMD Num>")
      sys.exit(1)

  print 'The script will search the file', sys.argv[1] ,'with' ,sys.argv[2], sys.argv[3]


if __name__ == '__main__':
  main()
  result=Queue.Queue() 
  pool = Pool()  ## This will define the number of the con-current fgrep process ,we can put Pool(3) if you just want to use 3 thread, the default Pool() will start up same process as CPU cores
  master_log_dir = os.path.dirname(sys.argv[1])
  master_log_file  = os.path.basename(sys.argv[1]) 
  cmd = 'ls '+master_log_dir+'/*part*'
#  print "The command to run is", cmd
  (status_ls, output) = commands.getstatusoutput(cmd)
  if status_ls:
    splitfile(sys.argv[1])
  else:
    print "In the master log direcotory, it contains *part* files, thus the script will not split the master log again"
  (status_ls, output) = commands.getstatusoutput(cmd)
  split_files=output.split()
  
  def pool_th():
    for i in split_files:
	try:
	   result.put(pool.apply_async(fgrep_function, args=(i,sys.argv[2],sys.argv[3],)))
	except:
	   break
    try:
      pool.close()
    except OSError:
      pass
    try:
      pool.join()
    except OSError:
      pass

  def result_th():
    global split_file
    global status
    while 1:
      (status,output,split_file)=result.get().get()
      if status == 0:
        try:
          pool.terminate()
        except OSError:
          pass
        try:
          pool.join()
	except OSError:
          pass 
        print "The splitted log which contains the SQL is :",split_file
        break

  t1=threading.Thread(target=pool_th)
  t2=threading.Thread(target=result_th)
  t1.start()
  t2.start()
  t1.join()
  if status == 0:
    get_query_from_match_split_file(split_file,sys.argv[2],sys.argv[3])
    os._exit(1)
  else:
    print "Cannot find query in the master log"
    os._exit(1)
