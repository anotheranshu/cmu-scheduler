import re

f = open("dict.txt", 'rb')

s =  eval(f.read())


def notRightDescription(description,key):
	if description == "":
		return False
	delimiters = " ", ")", "("
	isOkay = False
	regexPattern = '|'.join(map(re.escape, delimiters))
	words  = re.split(regexPattern,description)
	new_words = [i for i in words if len(i) != 0]
	for word in new_words:
		if not(word.isdigit() or word == "or" or word == "and"): #
			isOkay = True
	if not(isOkay):
		return True
	return False
	#print new_words
	#print key

def fixDict(d):
	for key,value in d.items():
		description = value[5]
		preReq = value[9]
		#print "CID", key
		#print "DESCRIPTION:", description.encode('utf-8')
		#print "prereqs:", preReq.encode('utf-8')
		if (notRightDescription(description,key)):
			value[5] = preReq
			value[9] = description
			d[key] = value
			#print description.encode('utf-8')
	with open("dict.txt", "w") as myfile:
         myfile.write(repr(d))


#17619