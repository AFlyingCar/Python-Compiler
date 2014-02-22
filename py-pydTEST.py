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

for item in os.listdir("C:\\Python27\\libs"):
	include[item] = "C:\\Python27\\libs"

#for item in os.listdir(os.getcwd() + "\\src"):
finder.run_script("HelloWorld.py")

os.chdir("bin")

print "Loaded modules: "
for name, mod in finder.modules.iteritems():
	print '%s: ' % name,
	print ','.join(mod.globalnames.keys()[:3])
	modules.append(name)

print '-'*50
print "Modules not imported: "
print '\n'.join(finder.badmodules.iterkeys())

print "\n\n"
for item in modules:
	print item

for item in modules:
	for root, dirs, files in os.walk("C:\\Python27\\Lib"):
		for file in files:
			if file == item + ".py":
				print file
				include[file] = root

for item in include:
	print "copy " + item + " " + os.getcwd() + "\\bin"
	if include[item].endswith("\\Lib"):
		if not os.path.exists(os.getcwd() + "\\Lib"):
			os.mkdir(os.getcwd() + "\\Lib")
		os.system("copy " + include[item] + "\\" + item + " " + os.getcwd() + "\\bin" + "\\Lib")
	
	else:
		path = include[item][include[item].index("\\Lib") + len("\\Lib"):]
		folder = path.split("\\")[len(path.split("\\")) - 1]

		for item in path.split("\\"):
#			if item not in os.path.exists(os.getcwd() + path):
			if not os.path.exists(os.getcwd() + path[path.index("\\" + item):]):
				print path[path.index("\\" + item):]
				dirs = os.getcwd()
				for item in path[path.index("\\" + item):].split("\\"):
					if item == "":
						continue
					os.mkdir(item)
					os.chdir(item)
#					dirs = dirs + "\\" + item
#					print dirs
				os.chdir(dirs)

		os.system("copy " + include[item] + "\\" + item + " " + os.getcwd() + path)

print include

nuclear = u'\u2622'