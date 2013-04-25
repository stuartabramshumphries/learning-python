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


#         if '<td class="RCelement"><a href="' in line:
#	 	print line
#	 elif re.search('\s+\<\/table>',line):
#	 	print "AAAARGH"
	fd.close
#	os.remove(filedogname)
	fd2.close
	analyse_data(dogname)

def analyse_data(dogname):
	''' this function analyses the dogs racing history
	shall we graph this and the moving average?
	certainly want to do a rating '''
	import re
	print "in analyse_data "
	filedogname2=dogname + "-race-history.txt"
	fd2=open(filedogname2,"r")
	data=fd2.readlines()
	# enumerate starts at line 0
	for i,line in enumerate(data):
		 if '<td class="RCelement"><a href="res_race_result.php?raceid=' in line:
		   line=line.replace('<td class="RCelement"><a href="res_race_result.php?raceid=','')		   
		   line=line.replace('</a></td>','')
		   line=re.sub(r"^.*\>",'',line)
                   print i,line
		 elif i == 1 or (i+1) % 16 == 0:
		   line=re.sub(r"^.*>",'',line)
		   line2=re.sub(r'</td class="RCelement">','',line)
		   line3=re.sub(r"</td>$",'',line2)
		   print "dist ",i,line3
		 elif i == 3 or (i+3) % 16 ==0:
		   line=re.sub(r"^.*>",'',line)
		   line2=re.sub(r'</td class="RCelement">','',line)
		   line3=re.sub(r"</td>$",'',line2)
		   print i,line3
		 elif i == 4 or (i+4) % 16 == 0:
		  line=re.sub(r"^.*>",'',line)
		  line2=re.sub(r'</td class="RCelement">','',line)
		  line3=re.sub(r"</td>$",'',line)
		  print i,line3
		 elif i== 9 or (i+9) % 16 ==0:
		  line=re.sub(r"^.*>",'',line)
		  line2=re.sub(r'</td class="RCelement">','',line)
		  line3=re.sub(r"</td>$",'',line2)
		  print i, line3
		 elif i == 12 or (i + 12) % 16 ==0:
		  line=re.sub(r"^.*>",'',line)
		  line2=re.sub(r'</td class="RCelement">','',line)
		  line3=re.sub(r"</td>$",'',line2)
		  print i, line3
		 elif i == 13 or (i + 13) % 16 ==0:
		  line=re.sub(r"^.*>",'',line)
		  line2=re.sub(r'</td class="RCelement">','',line)
		  line3=re.sub(r"</td>$",'',line2)
		  print i, line3
	# what I want here is to extract the racehistory into an array
	#	lines of interest
	# this info repeats every 16 lines until the EOF
	date=0
	dis=1
	brk=3
	pos=4
	tim=9
	grade=12
	calctim=13
	
	fd2.close()
getdognames()
