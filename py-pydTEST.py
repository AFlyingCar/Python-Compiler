#Test for converting *.py files to *.pyd files
import os
from modulefinder import ModuleFinder

#modules = dir()

modules = []
include = {}
finder = ModuleFinder()

if not os.path.exists(os.getcwd() + "\\bin"): #generate \\bin file
	os.mkdir(os.getcwd() + "\\bin")
	print "Generating \\bin"

finder.run_script("HelloWorld.py")

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
for name, mod in finder.modules.iteritems():
	print '%s: ' % name,
	print ','.join(mod.globalnames.keys()[:3])
	modules.append(name)

print '-'*50
#print "\nModules not imported: "
#print '\n'.join(finder.badmodules.iterkeys())

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

nuclear = u'\u2622'