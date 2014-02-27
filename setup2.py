#Tyler Robbins
#2/20/14
#Python Script Packager
#This program will package python scripts into *.ppr files.

#*.ppr file structure:
	#*.ppr
		#src
			#source code in *.pyc (bytecode) files
		#bin
			#python libraries as *.pyd files
		#run.py
			#Executees bytecode in ./src

import dis
import shutil
import os, sys, getopt
import zipfile
import importlib
import py_compile
import platform as plat #Not currently being used. Will be used for multi-platform functionality later
from modulefinder import ModuleFinder

loc = os.getcwd() #gets current directory
help = __file__.split("\\")[len(__file__.split("\\")) - 1] + " -i *.py"
name = ""
modules = []
include = {}
finder = ModuleFinder()


if len(sys.argv) > 1: #if the user passes filename(s) through the terminal
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile="]) #get parameters passed by user
	except getopt.GetoptError:
		print help
		sys.exit()

	for opt, arg in opts:
		if opt == '-h': #print what to do
			print help
			sys.exit()

		elif opt in ('-i', '--ifile'): #if the user inputs a filename
			name = arg

		else: #if the user inputs something that isn't an option
			print "GenericError"
			print help
			sys.exit()

else: #if the user runs the program without passing args through the terminal
	name = raw_input("Name of file to package: ")

if not name.endswith(".py"):
	print "FileError: Can only package and *.py files."
	sys.exit()

print "Filename: " + name + "\n"

######Get raw name without extension######
NewName = name.split(".", len(name.split(".")) -1)[0]
print NewName #debug message

######Make run.bat######
content = """@echo off
SET SAVE=%PYTHONPATH%
SET PYTHONPATH=\\.\\bin
.\\src\\""" + name + """
SET PYTHONPATH=%SAVE%"""

open("run.bat", "w").write(content)

######Make \\bin folder######

if not os.path.exists(os.getcwd() + "\\bin"): #generate \\bin file
	os.mkdir(os.getcwd() + "\\bin")
	print "Generating \\bin"

finder.run_script(name)

os.chdir("bin")

if not os.path.exists(os.getcwd() + "\\Lib"):
	os.mkdir(os.getcwd() + "\\Lib")
	print "Generating \\bin\\Lib"

if not os.path.exists(os.getcwd() + "\\libs"):
	os.mkdir(os.getcwd() + "\\libs")
	print "Generating \\bin\\libs"

for root, dirs, files in os.walk("C:\\Python27\\libs"):
	for file in files:
		print "Copying " + file + " "*4 + "-"*5 + " "*4 + os.getcwd() + "\\libs"
		os.system("copy " + root + "\\" + file + " " + os.getcwd() + "\\libs")

print "\nIndexing loaded modules: \n"
for foo, mod in finder.modules.iteritems():
	print '%s: ' % foo,
	print ','.join(mod.globalnames.keys()[:3])
	modules.append(foo)

print '-'*50

print "\nLoaded modules: \n[",
for item in modules:
	print item + ", ",
print "]"

for item in modules:
	for root, dirs, files in os.walk("C:\\Python27\\Lib"):
		for file in files:
			if file == item + ".py":
				print file
				include[file] = root

print '-'*100

root = os.getcwd() + "\\Lib"

#If it turns out that the Python root files need to be in the same file structure, copy the directory tree in '\Lib'
#instead of copying each folder separately and placing each file in it's respective folder separately.

print "Copying Python modules"
for item in include:
	print "copying " + item
	print "Origin: " + include[item]
	os.system("copy " + include[item] + "\\" + item + " " + root)
	print "New location: " + root

print "Finished copying loaded modules into " + root

os.chdir(loc)

######Make \\src folder######
if name in os.listdir(loc):
	content = open(name, "r").read() #open filename
	content = content.split("\n") #split code at every line

else:
	print "No such file or directory: '" + name + ".'"

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

######Generate \\src directory######
if not os.path.exists(os.getcwd() + "\\src"):
	os.mkdir("src")
	print "Generating \\src"

######Find Python source files to compile int bytecode######
for item in os.listdir(loc):
	if item == os.path.basename(__file__): #ignore self
		print "Ignoring /" + item
		continue

	elif item not in name: #ignore all but selected files
		print "Ignoring /" + item
		continue

	elif item.endswith(".py"): #only compile *.py files
		try:
			py_compile.compile(item)

		except Exception as e:
			print e

		#Packaging messages
		print "Compiling source"
		print "./" + item + "     ------>     " + item[:len(item) - 3] + ".pyc"
		dis.dis(item[:len(item) - 3])

		if item[:len(item) - 3] + ".pyc" in os.listdir(loc):
			os.chdir("src")
			print "Moving " + loc + "\\" + item[:len(item) - 3] + ".pyc     ------>     " + os.getcwd() #Package message
			os.rename(loc + "\\" + item[:len(item) - 3] + ".pyc", os.getcwd() + "\\" + item[:len(item) - 3] + ".pyc") #move *.pyc file to //src
			os.chdir(loc)
	
	else: #ignore all other files
		print "Ignoring /" + item
		continue

######Generate *.zip file######
#Note: This code cannot create 
print "Generating " + NewName + ".zip"
zf = zipfile.ZipFile(NewName + ".zip", 'w')

for dirname, subdirs, files in os.walk("src"): #write \\src to the *.zip
	zf.write(dirname)
	for filename in files:
		zf.write(os.path.join(dirname, filename))

for dirname, subdirs, files in os.walk("bin"): #write \\bin to the *.zip
	zf.write(dirname)
	for filename in files:
		zf.write(os.path.join(dirname, filename))

zf.write("run.bat") #write ./run.py to the *.zip Note: commented out until the generator for ./run.py has been completed
zf.close()

os.rename(loc + "\\" + NewName + ".zip", loc + "\\" + NewName + ".ppr") #change *.zip to *.ppr

shutil.rmtree('src')
shutil.rmtree('bin')
os.remove('run.bat')

print content
print modules

nuclear = u'\u2622'