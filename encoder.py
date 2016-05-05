# By Kishoj Bajracharya
import random
import numpy
from decimal import *


# Code for random linear coding
def linearCode(x, y):
	ilist = []
	a = 1*x + 1*y
	b = 2*x + 1*y
	ilist.append(numpy.float64(1))
	ilist.append(numpy.float64(1))
	ilist.append(numpy.float64(a))

	ilist.append(numpy.float64(2))
	ilist.append(numpy.float64(1))
	ilist.append(numpy.float64(b))
	return ilist

def encode(x, y):
	li = linearCode(x, y)
	#for a in li: 
	#	print a
	listOfEqns = split(3, li)
	return listOfEqns

def split(n, iter, fill=None):
	return [iter[i:i+n] + [fill] * (i + n - len(iter))
			for i in xrange(0, len(iter), n)]

def ConcatListElements(alist):
	p = ''
	for x in alist:
		p += x
	return p

def toHex(s):
	lst = []
	for ch in s:
		hv = hex(ord(ch)).replace('0x', '')
		if len(hv) == 1:
			hv = '0'+hv
		lst.append(hv)
	return reduce(lambda x,y:x+y, lst)

def ListOfCharToListOfInt(alist):
	iList = []
	for x in alist:
		# char to hex
		q = toHex(x)
		#print q 
		#p = int('0x48', 16)
		# Hex to int		
		p = int(q, 16)
		#print p
		iList.append(p)
	return iList

def ListOfIntToListOfString(alist):
	iList = []
	for x in alist:
		iList.append(chr(x))
	return iList


def StringDecodedToListof4(astring):# split the string into pure numbers. four string of pure numbers.
	Decodedlist = []
	c = astring.replace("], [", ', ')
	d = c.replace("[[", '[')
	e = d.replace("]]", ']')
	f = e.replace(", ", ',')
	print f
	f = e.split(',')
	for x in f:
		y = x.strip('][ ')## remove the "]["
		z = float(y)
		Decodedlist.append(z)
	listOfEqns = split(3, Decodedlist)
	return listOfEqns



# Initial data from the three different source nodes
# Say data from node A
def get_raw_data(a, b):

	# Packets whose values are conveted into the decimal values
	p = ListOfCharToListOfInt(a)
	#print p
	q = ListOfCharToListOfInt(b)
	#print q

	i = 0

	# list containing decoded packets
	listAns = []

	# Perform an encoding operation using Random Linear Coding
	encodedlist = []

	for x in p:
		# Mix the packets from the list of 3 packets
		listOfVector = encode(x, q[i])
		i = i + 1
		#print 'List of Encoded data'
		print listOfVector
		encodedlist.append(listOfVector)

	#print encodedlist
	encoded_mess = str(encodedlist)
	print 'Encoded Message'
	print encoded_mess
	return encoded_mess
