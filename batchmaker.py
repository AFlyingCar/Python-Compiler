#Tyler Robbins
#2/23/14
#Batch Maker
#This will generate *.bat files that will run with PYTHONPATH set to \\bin

import os, sys

loc = os.getcwd()

try:
	os.chdir(os.getcwd() + "\\src")
except Exception as e:
	print e
	sys.exit()

for item in os.getcwd():
	if item.endswith(".py"):
		pass

content = """SET SAVE=%PYTHONPATH%"""

print content

nuclear = u'\u2622'