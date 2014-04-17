# Justin Frye jmfrye
# 4-16-2014
# 15-221 Spring 2014
# getCourses.py

import string

def mergeAnd(l, r):
	def addElem(e,l):
		def combine(lElem):
			eVar = e if type(e) == list else [e]
			lElemVar = lElem if type(lElem) == list else [lElem]
			return eVar + lElemVar
		return map(combine, l)
	
	nestedPairs = map(lambda lElem: addElem(lElem, r), l)
	pairs = []
	for i in xrange(len(nestedPairs)):
		for j in xrange(len(nestedPairs[i])):
			pairs += [nestedPairs[i][j]]

	return pairs

def testMergeAnd():
	assert(mergeAnd([],[]) == [])
	assert(mergeAnd([1,2,3], []) == [])
	assert(mergeAnd([1,2], [3,4]) == [ [1,3], [1,4], [2,3], [2,4] ])
	assert(mergeAnd([1,2,3], [4,5]) == [ [1,4], [1,5], [2,4], [2,5], [3,4], [3,5] ])

def mergeOr(l, r):
	return l + r

def split(s):
	parenCnt = 0
	for i in xrange(len(s)):
		# Track paren count
		if (s[i] == "("):
			parenCnt += 1
		elif (s[i] == ")"):
			parenCnt -= 1
		# Return logical operator at outermost parent level
		if (i > 0 and i < (len(s) - 1) and s[i] == " " and parenCnt == 0):
			operator = s[i+1:] # returns either "and..." or "or..."
			if (operator[0:3] == "and"):
				return (s[:i+1], "and", s[i+5:])
			elif (operator[0:2] == "or"):
				return (s[:i+1], "or", s[i+4:])
			else: 
				return None
	return (s,None,"")

def noLetters(s):
    for c in string.ascii_letters:
    	if c in s:
    		return False
    return True

def getCourses(s):
	# Remove extraneous spaces

	s = s.lstrip(" ")
	s = s.rstrip(" ")

	# Remove outer parens if they exist
	if (s[0] == "(" and s[-1] == ")"):
		s = s[1:-1]

	# Base case: course number	
	if (noLetters(s)):
		s = s.lstrip("(")
		s = s.rstrip(")")
		try:
			return [int(s)]
		except:
			print "Not valid number input"
			return None

	# Recursive case: courses connected by logical operators
	else:
		(l,op,r) = split(s)
		left = getCourses(l)
		right = getCourses("(" + r + ")")
		if (op == "and"):
			return mergeAnd(left, right)
		elif (op == "or"):
			return mergeOr(left, right)
		else:
			print "OpError: ", op

def prereqs(s):
	if s == "None":
		return []
	s = "(" + s + ")"
	return getCourses(s)

def testPrereqs():
	assert(prereqs("(15210 and 15251) or (15212)") == [ [15210, 15251], 15212 ])
	assert(prereqs("15110 and 15112 and 15122") == [ [15110, 15112, 15122] ])
	assert(prereqs("(15210 or 15251) and (15212) and (15214)") == 
		[[15210, 15212, 15214], [15251, 15212, 15214]])
	assert(prereqs("(15210 or (15213 and 15214) or 15251) and (15212)") == 
		[ [15210,15212], [15213,15214,15212], [15251, 15212] ])
	print "PASSED!"

def testAll():
	testMergeAnd()
	testPrereqs()
	print "PASSED!"

#testAll()