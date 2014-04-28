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

    # Generate all possible "pairs" (possibly more than 2 courses) fulfilling AND requirement
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

def getCourses(s,d):
    # Remove extraneous spaces from beginning/end of prereq string
    s = s.lstrip(" ")
    s = s.rstrip(" ")

    # Remove outer parens from prereq string if they exist
    if (s[0] == "(" and s[-1] == ")"):
        s = s[1:-1]

    # Base case: end of prereq string (right side)
    if (s == ""):
        return None
    # Base case: course number - no logical operators remaining
    if (noLetters(s)):
        # Remove parens from the course number
        s = s.lstrip("(")
        s = s.rstrip(")")
        # Then turn into integer and return
        try:
            return [int(s)]
        except:
            print "Not valid number input: %s" % (s)
            return None

    # Recursive case: courses connected by logical operators
    else:
        # Split the string around the leftmost logical operator (and, or)
        # for which the parens are balanced, e.g. (15418 and 15210) or (15210) splits on the "or"
        (l,op,r) = split(s)
        
        left = getCourses(l,d+1)
        # Add parens to the right side of the prereq string because getCourses removes
        # outer parens from all inputs for consistency
        right = getCourses("(" + r + ")",d+1)
        if (op == "and"):
            return mergeAnd(left, right)
        elif (op == "or"):
            return mergeOr(left, right)
        # At the right end of the prereq string
        elif (op == None and r == ""):
            return left
        else: # Some error occurred parsing the string
            print "OpError: ", op

def prereqs(s):
	if s.strip() == "":
		return []
	if s == "None":
		return []
	s = "(" + s + ")"
	return getCourses(s,0)

def testPrereqs():
    assert(prereqs("(15210 and 15251) or (15212)") == [[15210, 15251], 15212 ])
    assert(prereqs("15110 and 15112 and 15122") == [[15110, 15112, 15122]])
    assert(prereqs("(15210 or 15251) and (15212) and (15214)") == [[15210, 15212, 15214], [15251,15212, 15214]])
    assert(prereqs("(15210 or (15213 and 15214) or 15251) and (15212)") == [[15210,15212], [15213,15214,15212], [15251, 15212]])
    assert(prereqs("(15121 or 15122) and (21127 or 15151)") == [[15121,21127], [15121,15151], [15122,21127], [15122,15151]])
    assert(prereqs("(15212 or 15122) and (21127 or 15151) and (15110)") ==
                   [[15212,21127,15110], [15212,15151,15110], [15122,21127,15110], [15122,15151,15110]])
    assert(prereqs("(15212 or 15122 or 15410) and (21127 or 15151) and (15110)") ==
          [[15212,21127,15110], [15212,15151,15110], [15122,21127,15110], [15122,15151,15110], [15410,21127,15110], [15410,15151,15110]])
    assert(prereqs("(15212 or 15122 or 15410) and (21127 or 15151) and (15110 or 15112)") ==
          [[15212,21127,15110],[15212,21127,15112], [15212,15151,15110], [15212,15151,15112], [15122,21127,15110], [15122,21127,15112],
           [15122,15151,15110], [15122,15151,15112], [15410,21127,15110], [15410,21127,15112], [15410,15151,15110], [15410,15151,15112]])
    print "PASSED!"

def testAll():
	testMergeAnd()
	testPrereqs()
	print "PASSED!"

testAll()