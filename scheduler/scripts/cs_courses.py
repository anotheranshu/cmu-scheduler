from lxml import html
import requests
import urllib
from pyquery import PyQuery as pq

#page = requests.get('http://coursecatalog.web.cmu.edu/schoolofcomputerscience/')
#tree = html.fromstring(page)

url = 'http://coursecatalog.web.cmu.edu/schoolofcomputerscience/'
content = urllib.urlopen(url).read()
tree = html.fromstring(content)

d = pq(tree)
#print d
# for pre in d('.codecol'):
# 	try:
# 		print d(pre).text()
# 		print d(pre).parent().parent().parent().find('td[colspan]').text()
# 	except:
# 		continue


for test4 in d('td[colspan]'):
	print d(test4).text()

test = tree.find_class('codecol')

# def f(x):
# 	if x == "\n":
# 		return False
# 	else:
# 		return True

# t = tree.cssselect('td:nth-child(1) , .codecol .code')
# #print t[0].xpath('//text()')
# final = t[0].xpath('//text()')
# p = filter(f,final)		

# tester = tree.cssselect('p+ .sc_courselist .codecol .code , h3+ .sc_courselist tbody:nth-child(1) td , h3+ .sc_courselist .codecol .code')
# print tester[0].xpath('//text()')
# #print p
# #q = t.xpath('//text()')
# #filtered = filter(f,q)
# #i = 0
# #for t in test:
# #	i = i + 1
# #	if (i == 2):
# #		break
# #	q = t.xpath('//text()')
# #	print q

b6 = tree.xpath('//td/a/text()')
print b6



