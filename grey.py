#!/usr/bin/python
import urllib
import re
import os
dognames="./dognames.txt"

def readdogs(dogname):
	'''  this function reads the primary web page for eachdog '''
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
	import re
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
	   fd2.write(line)
	   flag = 0
	 if re.search('\s+\<\/table>',line): 
	   flag = 1
	 if not flag and not '<td class="RCelement"><a href="' in line:
	   fd2.write(line)


	fd.close
	os.remove(filedogname)
	fd2.close
	analyse_data(dogname)

def analyse_data(dogname): 
	'''  this function extracts the dog data we want from its history '''
	filedogname2=dogname + "-race-history.txt"
	fd=open(dogname +"-data.txt","w")
	fd2=open(filedogname2,"r")
	data=fd2.readlines()

	for i,line in enumerate(data):
		 if '<td class="RCelement"><a href="res_race_result.php?raceid=' in line:
		   line=line.replace('<td class="RCelement"><a href="res_race_result.php?raceid=','')		   
		   line=line.replace('</a></td>',' ')
		   line=re.sub(r"^.*\>","",line)
                   fd.write("\n"),
                   fd.write(line.strip()),
                   fd.write(" "),
		 
		 else:
		  for j in [1,3,4,9,12,13]:
		   if i == j or (i-j) % 16 == 0:
		     line=line.replace('<td class="RCelement">','')
		     line=re.sub(r"</td>$",'',line)
		     fd.write(line.strip()),
		     fd.write(" "),

	
	fd.close()
	fd2.close()
	os.remove(filedogname2)
getdognames()
