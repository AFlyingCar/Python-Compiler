#Tyler Robbins
#2/20/14
#Setup
#This program will build *.par files for python. This is entirely experimental

#*.par file structure:
	#*.par
		#src
			#source code in *.pyc (bytecode)
		#bin
			#python libraries as *.pyd files
		#run.py
			#Executees bytecode in ./src

import os
import zipfile
import importlib
import py_compile
import dis

loc = os.getcwd() #gets current directory

name = raw_input("Name of file to compile: ") #path to source

if name in os.listdir(loc):
	content = open(name, "r").read() #opens filename

else:
	print "No such file or directory, '" + name + ".'"

name = name.split(".", len(name.split(".")) -1)[0] #get raw name without extension (might not be needed)
print name #debug message

content = content.split("\n") #split code at every line

for item in content: #remove comments from code
	if "#" in item:
		content.remove(item)

content = filter(None, content) #remove empty strings from 'content'

#####Get modules to import#####
for item in content: 
	if "import" in item:
		modules = item.split("import", 1)[1].split(",")

for item in modules: #remove spaces
	if " " in item:
		modules[modules.index(item)] = item.replace(" ", "")


if not os.path.exists(os.getcwd() + "\\src"): #generate \\src file
	os.mkdir("src")
	print "Making \\src"

for item in os.listdir(loc): #compile source code into *.pyc files
	if item == os.path.basename(__file__): #ignore compiler
		print "Ignoring /" + item
		continue

	elif item.endswith(".py"): #only compile *.py files
		try:
			py_compile.compile(item)

		except Exception as e:
			print e

		print "Compiling source"
		print "./" + item + "     ------>     " + item[:len(item) - 3] + ".pyc" #Compile messages
		dis.dis(item[:len(item) - 3])

		if item[:len(item) - 3] + ".pyc" in os.listdir(loc):
			os.chdir("src")
			print "Moving " + loc + "\\" + item[:len(item) - 3] + ".pyc     ------>     " + os.getcwd() #Compile messages
			os.rename(loc + "\\" + item[:len(item) - 3] + ".pyc", os.getcwd() + "\\" + item[:len(item) - 3] + ".pyc") #move *.pyc file to //src
			os.chdir(loc)
	
	else: #ignore all other files
		print "Ignoring /" + item
		continue

print "Generating " + name + ".zip"
zf = zipfile.ZipFile(name + ".zip", 'w') #generate zip file

for dirname, subdirs, files in os.walk("src"):
	zf.write(dirname)
	for filename in files:
		zf.write(os.path.join(dirname, filename))

for dirname, subdirs, files in os.walk("bin"):
	zf.write(dirname)
	for filename in files:
		zf.write(os.path.join(dirname, filename))

zf.write("run.py")
zf.close()

os.rename(loc + "\\" + name + ".zip", loc + "\\" + name + ".par")

print content
print modules

nuclear = u'\u2622'