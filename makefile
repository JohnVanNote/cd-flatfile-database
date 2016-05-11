#
# makefile
#
# Makefile for cddb utility
#
# Created by John Van Note
# Created on 12/01/11
#

class_file = album.py
run_file = cddb.py

.SILENT : build

view : $(run_file)
	cat $(run_file) $(class_file) | less

build : $(class_file)
	python $(run_file) $$EXT

.PHONY : clean
clean :
	- \rm *.pyc

#eof
