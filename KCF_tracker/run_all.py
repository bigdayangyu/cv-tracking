import os
import sys
import glob

root_dir = "/home/christina/Documents/computer_vision/OTB50/"
datasets = glob.glob( root_dir +"*")
print(len(datasets))

for folder in datasets:
	print(folder)
	name = folder[len(root_dir):]
	execute = 'python3 ./myKCF/run.py '+folder+' '+name
	os.system(execute)
	print("finished running %s" %name)

