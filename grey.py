#!/usr/bin/python
import urllib
import sys
import re
import os
from movingaverage import *
from multiprocessing import Process

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
		print n
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
		   if i != 0:
		    fd.write("\n")
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
	calc_moving_average(dogname)

def calc_moving_average(dogname):
      
      ''' basically movingaverage(data,period) , where data is a list/tuple? '''
      
      ratings={
      'A1':{1:170,2:152,3:143,4:133,5:122,6:106},
      'A2':{1:152,2:140,3:126,4:113,5:101,6:87},
      'A3':{1:145,2:130,3:118,4:107,5:97,6:86},
      'A4':{1:138,2:125,3:113,4:102,5:87,6:73},
      'A5':{1:133,2:118,3:106,4:95,5:85,6:71},
      'A6':{1:125,2:110,3:98,4:89,5:76,6:65},
      'A7':{1:118,2:103,3:91,4:82,5:69,6:58},
      'A8':{1:99,2:86,3:77,4:66,5:53,6:42},
      'A9':{1:90,2:60,3:50,4:40,5:30,6:20},
      'A10':{1:80,2:60,3:50,4:40,5:30,6:20},
      'A15':{1:70,2:50,3:40,4:30,5:20,6:10},
      'B1':{1:60,2:50,3:40,4:30,5:20,6:10},
      'S1':{1:170,2:159,3:144,4:135,5:125,6:110},
      'S2':{1:151,2:135,3:123,4:107,5:96,6:82},
      'S3':{1:127,2:118,3:101,4:90,5:71,6:58},
      'S4':{1:105,2:99,3:64,4:64,5:34,6:34},
      'S5':{1:90,2:80,3:60,4:60,5:30,6:30},
      'S6':{1:80,2:70,3:50,4:50,5:20,6:20},
      'S7':{1:70,2:60,3:40,4:40,5:10,6:10},
      'KS':{1:138,2:125,3:113,4:102,5:87,6:73},
      'HP':{1:145,2:130,3:118,4:107,5:97,6:86},
      'D3':{1:133,2:118,3:106,4:95,5:85,6:71},
      'E1':{1:118,2:103,3:91,4:82,5:69,6:58},
      'H3':{1:118,2:103,3:91,4:82,5:69,6:58},
      'P3':{1:99,2:86,3:77,4:66,5:53,6:42},
      'IV':{1:170,2:152,3:143,4:133,5:122,6:106},
      'OR':{1:170,2:152,3:143,4:133,5:122,6:106}
      }
      period=4 # arbitrary here - maybe ask what moving average you want at the start?
      try:
       fd=open(dogname +"-data.txt","r")
       fd2=open("ratings.out.txt","a")
      except:
       pass
      
      dat=fd.readlines()
      data=[]
      for line in dat:
	 splitline=line.split()
	 if len(splitline) == 7:
	  pos=splitline[3]
	  grade=splitline[5]
	  pos=pos[:-2]
      	  pos=int(pos)
	  rat=ratings[grade][pos]
      	  if int(rat) != 0:
      	    data.append(rat)

      klist=list(movingaverage(data,period))
      v=(dogname,klist)
      value=str(v)
      fd2.write(value)
      fd2.write("\n")
      fd2.close()
      
def generate_html_graph():
      ''' prints moving average data to html file thats viewed in a browser '''
      try:
         txt=open("./header","r").read()
         txt2=open("./footer","r").read()
         fd=open("./graph.html","w")
      except:
         print "issues opening files\n"

      fd.write(txt)


      dogdat=[]
      text=open("ratings.out.txt","r").readlines()
      count=0
      for line in text:
      	count+=1
	line=re.sub("\'|\(|\[|\]|\)|\,","",line)
	dogdat.append(line.split())
      st1="\"['race #'\","
      fd.write(st1)
      for line in xrange(count):
	st2="\",'\",dogdat[line][0],\"'\","
	fd.write(st2)
      fd.write( "],")
      line=0
      for i in range(1,7):
       st3=" \"['\",i,\"'\",dogdat[line][i], \",\",dogdat[line+1][i],\",\",dogdat[line+2][i],\",\",dogdat[line+3][i],\",\",dogdat[line+4][i],\",\",dogdat[line+5][i],\"]\", "
       fd.write(st3) 
       if i<=5:
        fd.write( ",")
       else:
        fd.write( "]);")
      fd.write(txt2)
      fd.close()


''' add a check to see if file exists, then remove if it does, else it'll error here '''
#os.remove("ratings.out.txt")
#getdognames()
generate_html_graph()
