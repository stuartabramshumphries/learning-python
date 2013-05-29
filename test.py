#!/usr/bin/python
def doit():
	'''  this function extracts the dog data we want from its history '''
	dogname="fred"
        filedogname2=dogname + "-rh.txt"
        print "filename is ", filedogname2
        fd3=open("./frettenham+flyer-rh.txt","r")
	print fd3
        fd=open(dogname +"-data.txt","w")
	print fd3.name
	print fd3.fileno()
        data2=fd3.readlines()
	print data2
        fd3.close

doit()
