#Tyler Robbins
#2/23/14
#Batch Maker
#This will generate *.bat files that will run with PYTHONPATH set to \\bin

import os, sys

loc = os.getcwd()
name = raw_input("File name: ")

content = """@echo off
SET SAVE=%PYTHONPATH%
SET PYTHONPATH=\\.\\bin
.\\src\\""" + name + """
SET PYTHONPATH=%SAVE%"""

print content

open("run.bat", "w").write(content)

nuclear = u'\u2622'