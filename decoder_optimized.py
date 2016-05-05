import random
import numpy
from decimal import *

def StringDecodedToListof4(astring,numpacket):
	Decodedlist = []
	c = astring.replace("], [", ', ')
	d = c.replace("[[", '[')
	e = d.replace("]]", ']').replace("]], [[", ',')
	f = e.replace(", ", ',')
	print f
	f = e.split(',')
	for x in f:
		y = x.strip('][ ')
		z = float(y)
		Decodedlist.append(z)
	listOfEqns = split(numpacket+1, Decodedlist)
	print "List of equations", listOfEqns
	return listOfEqns

def ConcatListElements(alist):
	p = ''
	for x in alist:
		p += x
	return p
def split(n, iter, fill=None):
	return [iter[i:i+n] + [fill] * (i + n - len(iter))
			for i in xrange(0, len(iter), n)]

def ListOfIntToListOfString(alist):
	iList = []
	for x in alist:
		iList.append(chr(x))
	return iList

#Decodes using Gauss elimination method
def DecodeAtReceiver(listOfVector):
	a = numpy.array(listOfVector)
	rows=a.shape[0]
	columns=a.shape[1]
	print(a)
	answer = numpy.zeros(rows)
	# Eliminating variables
	for i in numpy.arange(0,columns): #variable to eliminate
		for j in numpy.arange(i+1,rows): #rows to eliminate said variable from
			tmp=a[i]*(-a[j][i]/a[i][i]) #multiply row
			a[j]=tmp+a[j] #add
	# Back substitute
	for i in (numpy.arange(rows).shape[0]-numpy.arange(rows)-1):
		if(i<columns-2):
			a[i][columns-1]=a[i][columns-1]-(sum(a[i])-a[i][i]-a[i][columns-1])

		#calculate ith variable
		answer[i]=a[i][columns-1]/(a[i][i])
		#substitute variable by
		#multiply rows starting with i-1, column i by answer[i]
		for j in numpy.arange(0,i):
			a[j][i]=a[j][i]*answer[i]
	return answer

def get_raw_encoded_data(encodedstringreceived, numpacket):
	# Encoded message got from network

	# Decoding Part
	#################################################################
	#decodeddatalist1 = []
	#decodeddatalist2 = []
	numpacket=2
	numpacketl=numpacket-1
	decodeddatalist = []


	# list containing decoded packets
	encoded_list = StringDecodedToListof4(encodedstringreceived,numpacket)
	print 'encoded list'
	print encoded_list

	listt = split(numpacket, encoded_list)
	print listt
	listAns =[]

	for listOfVector in listt:
		decoded = DecodeAtReceiver(listOfVector)
		print decoded

		y = []
		for x in decoded:
			y.append(int(round(x, 0)))
		print y
		listAns.append(y)

	ith=0
	abc = []
	decodeddata = ''
	decodeddatalist_temp=lists = [[] for i in range(numpacketl)]


	for ix in listAns:
		#print "shishiasidafgalsfguy"
		#print ix
		#print "shishiasidafgalsfguy"
		decodeddatalist_temp[ith-1] = ix
		print ''
		print 'Decoded data: '
		print 'Data from source ' #source node needs to be changed
		# Data in decimal value
		print decodeddatalist_temp[ith-1]
		abc =  ListOfIntToListOfString(decodeddatalist_temp[ith-1])
		print abc
		decodeddata = ConcatListElements(abc)
		print decodeddata
		ith+=1
		return decodeddata