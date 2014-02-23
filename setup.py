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
import os, sys, getopt
import zipfile
import importlib
import py_compile
import platform as plat #Not currently being used. Will be used for multi-platform functionality later

loc = os.getcwd() #gets current directory
help = __file__.split("\\")[len(__file__.split("\\")) - 1] + " -i *.py"
name = ""

if len(sys.argv) >= 1: #if the user passes filename(s) through the terminal
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile="])
	except getopt.GetoptError:
		print help
		sys.exit()

	for opt, arg in opts:
		if opt == '-h':
			print help
			sys.exit()
		elif opt in ('-i', '--ifile'):
			name = arg

		else:
			print "GenericError"
			sys.exit()

else: #if the user runs the program without passing args through the terminal
	name = raw_input("Name of file to package: ")

print "Filename: " + name + "\n"

if name in os.listdir(loc):
	content = open(name, "r").read() #open filename
	content = content.split("\n") #split code at every line

else:
	print "No such file or directory: '" + name + ".'"

name = name.split(".", len(name.split(".")) -1)[0] #get raw name without extension (might not be needed)
print name #debug message

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
	if item == os.path.basename(__file__): #ignore self
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

print "Generating " + name + ".zip"
zf = zipfile.ZipFile(name + ".zip", 'w') #generate zip file

for dirname, subdirs, files in os.walk("src"): #write \\src to the *.zip
	zf.write(dirname)
	
	for filename in files:
		zf.write(os.path.join(dirname, filename))

for dirname, subdirs, files in os.walk("bin"): #write \\bin to the *.zip
	zf.write(dirname)

	for filename in files:
		zf.write(os.path.join(dirname, filename))

zf.write("run.py") #write ./run.py to the *.zip
zf.close()

os.rename(loc + "\\" + name + ".zip", loc + "\\" + name + ".ppr") #change *.zip to *.ppr

print content
print modules

nuclear = u'\u2622'