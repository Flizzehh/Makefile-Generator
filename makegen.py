#!/usr/bin/python3

# Created by Ryan White
# 2017

import sys, os

def WriteMakefile(executable, standard, flags, files):
	file = open("makefile","w")
	
	file.write("CC=gcc\n")

	flagsString = "CFLAGS="
	for i in range(-1,len(flags)):
		if (i == -1):
			flagsString += "-" + standard + " "
		else:
			flagsString += flags[i]
			if (i < len(flags)-1):
				flagsString += " "
	file.write(flagsString+"\n\n")

	oFiles = []
	hFiles = []
	cFiles = []
	for inputFile in files:
		if (inputFile.split('.')[1] == "c"):
			cFiles.append(inputFile)
			oFiles.append(inputFile.split('.')[0] + ".o")
		elif (inputFile.split('.')[1] == "h"):
			hFiles.append(inputFile)
		else:
			print("Unknown file type: " + inputFile)
	
	oFileString = ""
	for i in range(len(oFiles)):
		oFileString += oFiles[i]
		if (i < len(oFiles)-1):
			oFileString += " "

	hFileString = ""
	for i in range(len(hFiles)):
		hFileString += hFiles[i]
		if (i < len(hFiles)-1):
			hFileString += " "

	file.write(executable + " : " + oFileString + "\n")
	file.write("\t$(CC) -o " + executable + " " + oFileString + "\n\n")

	for i in range(len(oFiles)):
		oFile = oFiles[i]
		cFile = cFiles[i]
		file.write(oFile + " : " + cFile + " " + hFileString + "\n")
		file.write("\t$(CC) $(CFLAGS) -c " + cFile + "\n\n")

	file.write("clean : \n")
	file.write("\trm " + executable + " " + oFileString)

	file.close()

def GetExecutableName():
	executableName = ""
	while True:
		print("What would you like your executable to be called?")
		executableName = input(">> ")
		print("Are you sure you want your executable to be: \"" + executableName + "\"? (Yes/No)")
		correct = input(">> ")
		correct = correct.lower()
		if (correct == "yes" or correct == "y"):
			break
		else:
			continue
	return executableName

def GetCompilerStandard():
	compilerStandards = ["ansi","c89","c90","c95","c99","c11"]
	compilerStandardSelection = ""
	while True:
		print("Using \"gcc\" compiler. Which standard would you like to use? (\"list\" to see all versions)")
		compilerStandardSelection = input(">> ")
		compilerStandardSelection = compilerStandardSelection.lower()
		if (compilerStandardSelection[0] == '-'):
			compilerStandardSelection = compilerStandardSelection.split('-')[1]
		if (compilerStandardSelection == "list"):
			for i in range(len(compilerStandards)):
				print("\t" + compilerStandards[i])
			continue
		else:
			if (compilerStandardSelection not in compilerStandards):
				print(compilerStandardSelection + " is not a recognized standard. Are you sure you would like to use it? (Yes/No)")
				customStandard = input(">> ")
				customStandard = customStandard.lower()
				if (customStandard == "yes" or customStandard == "y"):
					break
				else:
					compilerStandardSelection = ""
					continue
			else:
				print("Are you sure you want to use the " + compilerStandardSelection + " standard? (Yes/No)")
				correct = input(">> ")
				correct = correct.lower()
				if (correct == "yes" or correct == "y"):
					print("Using the " + compilerStandardSelection + " standard.")
					break
				else:
					continue
		break
	return compilerStandardSelection

def GetFlags():
	flags = []
	while True:
		print("Add any flags you would like to use separated by spaces. (Example: \">> Wall -o\")")
		print("A dash can be included before a flag if you wish but it is not necessary as it will be added automatically in the event of its absense.")
		flagInput = input(">> ")
		print("You are using the flags: \"" + flagInput + "\". Is this correct? (Yes/No)")
		correct = ""
		while True:
			correct = input(">> ")
			correct = correct.lower()
			if (not(correct == "yes" or correct == "y" or correct == "no" or correct == "n")):
				print("Invalid decision. Use \"Yes\" or \"No\"")
				continue
			else:
				break
		if (correct == "yes" or correct == "y"):
			break
		elif (correct == "no" or correct == "n"):
			continue
		break

	for flag in flagInput.split(' '):
		if (list(flag)[0] != '-'):
			formattedFlag = "-" + flag
			flags.append(formattedFlag)
		else:
			flags.append(flag)
	return flags

def OutputMakefileInformation(files):
	if (len(files) > 0):
		outputText = "Generating makefile for:\n"
		for i in range(len(files)):
			outputText += "\t" + files[i]
			if (i < len(files)-1):
				outputText += "\n"
		print(outputText)
	print("makefile will contain " + str(len(files)) + " files.")

def GetFiles(method):
	files = []
	if (method == 1):
		numIgnoredFiles = 0
		ignoredFilesString = "Ignoring files:\n"
		for dirFile in [f for f in os.listdir('.') if os.path.isfile(f)]: #walk(os.getcwd()):
			if (len(dirFile.split('.')) > 1 and dirFile.split('.')[1] == "c"):
				files.append(dirFile)
			elif (len(dirFile.split('.')) > 1 and dirFile.split('.')[1] == "h"):
				files.append(dirFile)
			else:
				numIgnoredFiles += 1
				ignoredFilesString += "\t" + dirFile + "\n"
		if (numIgnoredFiles > 0):
			print(''.join(list(ignoredFilesString)[:len(list(ignoredFilesString))-1]))
		OutputMakefileInformation(files)
		if (len(files) <= 0):
			print("ERROR: No .c or .h files found in this directory.")
			print("Stopping program...")
			sys.exit()
		return files
	elif (method == 2):
		if (len(sys.argv) <= 1):
			print("ERROR: You must provide files to generate a makefile.")
			print("Run this with the format: ./makegen.py <file1> <file2> ... <fileN>")
			print("Stopping program...")
			sys.exit()
		else:
			for arg in sys.argv[1:]:
				files.append(arg)
		OutputMakefileInformation(sys.argv[1:])
		return files
	else:
		print("ERROR: Unable to get files, unknown input method.")
		print("Stopping program...")
		sys.exit()

def GetMakefileInformation(getFilesMethod):
	
	files = GetFiles(getFilesMethod)
	executableName = GetExecutableName()
	compilerStandardSelection = GetCompilerStandard()
	flags = GetFlags()
	
	print("Generating makefile...")
	WriteMakefile(executableName, compilerStandardSelection, flags, files)
	print("Makefile created.")
		
def main():

	if (sys.version_info[0] < 3):
		print("ERROR: Python 3 or greater is required.")
		sys.exit()

	while True:
		print("\nChoose file input method 1 or 2 (Enter \"1\" or \"2\")")
		print("\t1. Automatically generate makefile using files in the current directory.")
		print("\t2. Input files manually as arguments.")
		fileInputMethod = input(">> ")
		try:
			fileInputMethod = int(fileInputMethod)
		except:
			print("Incorrect method selection number. Enter \"1\" or \"2\")")
			continue
		if (fileInputMethod == 1 or fileInputMethod == 2):
			GetMakefileInformation(fileInputMethod)
			break
		else:
			print("Incorrect method selection number. Enter \"1\" or \"2\")")
			continue
		break

main()