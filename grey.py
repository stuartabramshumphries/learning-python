#!/usr/bin/python
import urllib
import re
import os
dognames="./dognames.txt"

def readdogs(dogname):
	'''  this function reads the primary page for eachdog '''
	dogname=dogname.replace(" ","+")
	f=urllib.urlopen("http://thedogs.co.uk/trap6/res_dog_search.php?txtDogName="+dogname)
	ddogname=dogname.rstrip()+".txt"
	webout=open(ddogname,"w")
	s=f.read()
	webout.write(s)
	f.close()
	webout.close()
	readdogspec(dogname)
	os.remove(ddogname)

def getdognames():
	''' this function reads a list of dognames from file '''
	dogname=open(dognames,"r").readlines()
	for n in dogname:
		readdogs(n)

def readdogspec(dogname):
	''' this function finds the specific URL for each dog and then downloads the dog history '''
	n2=open(dogname.rstrip()+".txt","r").readlines()
	for line in n2:
	    if "dogid" in line:
	    	datstring=line
		result=re.search('(.*)dogid=(.*)" onMouseOver(.*)',line)
		dogid=result.group(2)
		getdogdata(dogid,dogname)

def getdogdata(dogid,dogname):
	''' this function downloads the individual dogs race history, from its dogid '''
	dogname=dogname.rstrip()
	filedogname=dogname + "-racehist.txt"
	fd=open(filedogname,"w")
	ur="http://thedogs.co.uk/trap6/res_dog_history.php?dogid="+dogid
	f=urllib.urlopen(ur)
	data=f.read()
	fd.write(data)
	f.close()
	fd.close()
	extractdata(filedogname,dogname)

def extractdata(filedogname,dogname):
	'''  what this function does is to format the downloaded history - basically get rid of the extraneous html '''
	flag = 1
	fd=open(filedogname,"r")	
	filedogname2=dogname + "-race-history.txt"
	fd2=open(filedogname2,"w")	
	data=fd.readlines()
	for line in data:
	 if '<td class="RCelement"><a href="' in line:
	   flag = 0
	 if re.search('\s+\<\/table>',line): 
	   flag = 1
	 if not flag and not '<td class="RCelement"><a href="' in line:
	   fd2.write( line )


#         if '<td class="RCelement"><a href="' in line:
#	 	print line
#	 elif re.search('\s+\<\/table>',line):
#	 	print "AAAARGH"
	fd.close
	os.remove(filedogname)
	fd2.close

getdognames()
#print readdogs.__doc__
