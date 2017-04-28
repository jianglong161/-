#写一个脚本  
#      1.切换工作目录至/var  
#      2.依次向/var目录中的每个文件或子目录问好，形如：  
#        Hello,log  
#      3.统计/var目录下共有多个文件，并显示出来  
  
WORK_PATH=/var
COUNT=0
cd ${WORK_PATH}
for file in `ls `
	echo Hello,{$file} 	##依次像每个文件或子目录问号 
	let COUNT+=1 #let 是做数值运算   
done
echo  the number of files is ${NUM}	