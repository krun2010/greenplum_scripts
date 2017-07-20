#!/usr/bin/python
from multiprocessing import Pool
import sys
import os
import commands
import Queue
import threading
import time

def splitfile(dir):
  cmd = 'split -b 512m ' + dir + ' ' + dir + 'part'
  print "Command to run:", cmd   ## good to debug cmd before actually running it
  (status, output) = commands.getstatusoutput(cmd)
  if status:    ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    sys.exit(status)

def fgrep_function(split_file,conNum,cmdNum):
  cmd='fgrep'+ ' ' + conNum +','+ cmdNum +' '+ split_file
  print "ommand to run:", cmd
  (status, output) = commands.getstatusoutput(cmd)
  return (status,output,split_file)
 

def main():
  print 'We will search the file', sys.argv[1] ,'with' ,sys.argv[2], sys.argv[3]
#  splitfile(sys.argv[1])

if __name__ == '__main__':
  main()
  result=Queue.Queue() 
  pool = Pool(3)
  cmd = 'ls *part*'
  (status, output) = commands.getstatusoutput(cmd)
  split_files=output.split()
  def pool_th():
    for i in split_files:
	try:
	   result.put(pool.apply_async(fgrep_function, args=(i,sys.argv[2],sys.argv[3],)))
	except:
	   break

  def result_th():
    while 1:
      (status,output,split_file)=result.get().get()
      if status == 0:
        pool.terminate()
	print split_file
        break

  t1=threading.Thread(target=pool_th)
  t2=threading.Thread(target=result_th)
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  pool.join()

  	
