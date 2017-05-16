#!/usr/bin/env python
from os.path import isfile, join, isdir
import sys
import os
import shutil

metafileBasePath = sys.argv[1]

variableName = "DOCKERPARTS"
extraFilesDir = "extraFiles"
partsF="partFiles"

if variableName in os.environ :
	partsDir = os.environ[variableName]
	if partsDir != "" :
		# print directory
		partsDir = join(partsDir, partsF)
		print "parts directory : ", partsDir
		partsList = [f for f in os.listdir(partsDir) if isfile(join(partsDir, f)) and ".part" in f]
		# print available parts
		print "available docker parts : ", partsList

		#read in metafile
		metaRead = open("metafile", "r")
		metaLines = metaRead.read().splitlines()
		metaRead.close()
		print metaLines

		# check that all lines in metafile have corresponding lines
		goAhead = True
		count = 0
		sections = []
		extraFiles = []
		for j in metaLines:
			if j+".part" not in partsList and '#' not in j:
					goAhead = False
					sys.exit("Metafile line " + str(count) + ": " + j + ".part not found in " + partsDir)
			else:
				currPart = join(partsDir,j+".part")
				print currPart
				sect = open(currPart, 'r')
				sections += [sect.read()]
				sect.close()
				#check for COPY and ADD in section to make list of files to copy over
				sectionLines = sections[-1].split('\n')
				extraFileLines = [k for k in sectionLines if "COPY" in k or "ADD" in k]
				currExtraFiles = [k.split(' ')[1] for k in extraFileLines]
				#check all extra files are present
				verifiedFiles = []
				for k in currExtraFiles:
					if not isfile(join(partsDir,extraFilesDir,k)):
						print "Warning: Extra file " + k + " for line " + str(count) + " not found in " + join(partsDir,extraFilesDir)
					else:
						verifiedFiles += [k]
				print verifiedFiles
				extraFiles += verifiedFiles
				count += 1

		print "Metafile parsed"
		try:
			dockerfile = open("Dockerfile", 'w')
			
			for j in sections:
				dockerfile.write(j)
				dockerfile.write("\n\n")

			dockerfile.close()
		except:
			sys.exit("Exception when writing dockerfile")

		try:
			for j in extraFiles:
				print "Copying", join(partsDir,extraFilesDir,j), "to", join(metafileBasePath,j)
				shutil.copyfile(join(partsDir,extraFilesDir,j), join(metafileBasePath,j))
		except:
			sys.exit("Exception copying extra files")
	else:
		sys.exit(variableName + " is empty. Add directory to " + variableName + " environment variable")
else:
	sys.exit(variableName + " not found. Add " + variableName + " to environment variables")

