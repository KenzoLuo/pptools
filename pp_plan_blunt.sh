#!/bin/sh
v1=$1;
#v1:要处理的算例工作目录

cd $1
for dir in $(ls);do	
	cd $1/$dir
	echo "$dir postprocessing......"
	rm *.png
	python ~/work/tools/pp4ds2v.py blunt --resave $dir.plt --profile yes
	echo "$dir postprocessing complete!\n"
done
