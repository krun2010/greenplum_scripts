#!/bin/bash
generate_missing_extra_marker(){
	grep -n FAIL $1 -A 2 | grep 'missing or extraneous' -A 2 | grep ERROR > missing_extra_marker_line.txt
	cat ./missing_extra_marker_line.txt | while read i
	do 
#		echo $i
		start_line=`echo $i|awk -F '-' '{print $1}'`
		issue_count=`echo $i|awk '{print $5}'`
		issue_name=`echo $i| awk '{print $3}'`
		#echo '--------'
		echo $issue_name
		end_line=$(($start_line+$issue_count+1))
		echo $start_line
		echo $end_line
		echo $issue_count
		sed -n "${start_line},${end_line}"p $1 > ${issue_name}.out
		#sed_command= "sed -n \"${start_line}\,${end_line}p\ "$1 > ${issue_name}.out
		#echo ${sed_command}
	done
}


if [ $# -gt 0 ]
then
    if [ $# -eq 1 ]
    then
        generate_missing_extra_marker $1
    else
        echo "ERROR: You did not provide suffcient prameters"
    fi
else
    echo "No Prameter,exiting"
    exit
fi

