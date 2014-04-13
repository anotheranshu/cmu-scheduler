import re


def info():
	file = open('2010.SCS.BS.CS.MAJ.txt','rb')
	result = []
	category = ""
	classes = []
	#for line in file:
	line = file.readline()
	while (line  != ""):
		if len(line.strip()) == 0:
			line = file.readline()
			continue
		elif line[0] == "{": #category
			#print re.split(r"[{}]", line)[1]
			category = line
		elif category != "": #looking for classes
			#print line
			# splitted = re.split(r"[()]",line,1)
			# if (len(splitted) > 1):
			# 	finalStringArray = splitted[1].rsplit(")",1)
			# 	concatString = finalStringArray[0]
			# 	if len(finalStringArray) == 1: #go to next line
			# 		#print finalStringArray[0]
			# 		tempString = finalStringArray[0]
			# 		while len(tempString.rsplit(")",1)) == 1:
			# 			line = file.readline()
			# 			#tempString = re.split(r"[()]",line,1)
			# 			tempString = line
			# 			concatString = concatString + tempString
			# 		concatString = concatString.rsplit(")",1)[0]
			# 		print concatString
			# 	else:
			# 		print finalStringArray[0]
			# else:
			# 	concatString = line
			# 	print "LINE: %s" %line
			#if s.find('(')!=-1 # found
			concatString = ""
			while (line != "\r\n"):
				concatString = concatString + line
				line = file.readline()
			#print concatString
			classes.append((category,concatString))
			category = ""
		line = file.readline()
	print classes


info()
