#!/usr/bin/python
import urllib
import sys
import re
import os
from movingaverage import *
from multiprocessing import Process

dognames="./dognames.txt"


def analyse_data(dogname): 
	'''  this function extracts the dog data we want from its history '''
	filedogname2=dogname + "-rh.txt"
	#fd3=open(filedogname2,"r")
	#fd3=open("./frettenham+flyer-rh.txt","rb")
	fd=open(dogname +"-data.csv","w")
	fd3=open(dogname + "-rh.txt","r+")
	data=fd3.readlines()
	fd3.close()
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
	os.remove(filedogname2)
	calc_moving_average(dogname)
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
	count=0
	for n in dogname:
		count+=1
		print n
		readdogs(n)
#	if count >6:
#		print "number of dogs is ",count
#		print "currently only working on 6 dogs, will change in future!"
#		print "exiting - delete a dog from dognames.txt"
#		exit()

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
	filedogname2=dogname + "-rh.txt"
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


	fd.close()
	os.remove(filedogname)
	fd2.close()
	analyse_data(dogname)


def calc_moving_average(dogname):
      
      ''' basically movingaverage(data,period) , where data is a list/tuple? '''
      
      ratings={
      'A1':{1:138,2:120,3:112,4:94,5:86,6:78},
      'A2':{1:130,2:112,3:104,4:86,5:78,6:70},
      'A3':{1:122,2:104,3:96,4:78,5:70,6:62},
      'A4':{1:114,2:96,3:88,4:70,5:62,6:54},
      'A5':{1:106,2:88,3:80,4:62,5:54,6:46},
      'A6':{1:98,2:80,3:72,4:54,5:46,6:38},
      'A7':{1:90,2:72,3:64,4:46,5:38,6:30},
      'A8':{1:82,2:64,3:56,4:38,5:30,6:22},
      'A9':{1:74,2:56,3:48,4:30,5:22,6:14},
      'A10':{1:66,2:48,3:40,4:22,5:14,6:8},
      'A11':{1:58,2:40,3:32,4:14,5:6,6:6},
      'B2':{1:58,2:40,3:32,4:14,5:6,6:6},
      'S1':{1:122,2:104,3:96,4:78,5:70,6:62},
      'S2':{1:114,2:96,3:88,4:70,5:62,6:54},
      'S3':{1:106,2:88,3:80,4:62,5:54,6:46},
      'S4':{1:98,2:80,3:72,4:54,5:46,6:38},
      'S5':{1:90,2:72,3:64,4:46,5:38,6:30},
      'S6':{1:82,2:64,3:56,4:38,5:30,6:22},
      'S7':{1:74,2:56,3:48,4:30,5:22,6:14},
      'S8':{1:66,2:48,3:40,4:22,5:14,6:8},
      'S9':{1:58,2:40,3:32,4:14,5:6,6:6},
      'HP':{1:90,2:72,3:64,4:46,5:38,6:30},
      'H1':{1:82,2:64,3:56,4:38,5:30,6:22},
      'H2':{1:74,2:56,3:48,4:30,5:22,6:14},
      'H3':{1:66,2:48,3:40,4:22,5:14,6:8},
      'H4':{1:58,2:40,3:32,4:14,5:6,6:6},
      'OR':{1:138,2:120,3:112,4:94,5:86,6:78},
      'KS':{1:138,2:120,3:112,4:94,5:86,6:78},
      'P1':{1:90,2:72,3:64,4:46,5:38,6:30},
      'P2':{1:82,2:64,3:56,4:38,5:30,6:22},
      'P3':{1:74,2:56,3:48,4:30,5:22,6:14},
      'P4':{1:66,2:48,3:40,4:22,5:14,6:8},
      'P5':{1:58,2:40,3:32,4:14,5:6,6:6},
      'D1':{1:122,2:104,3:96,4:78,5:70,6:62},
      'D2':{1:114,2:96,3:88,4:70,5:62,6:54},
      'D3':{1:106,2:88,3:80,4:62,5:54,6:46},
      'D4':{1:98,2:80,3:72,4:54,5:46,6:38},
      'D5':{1:90,2:72,3:64,4:46,5:38,6:30},
      'IT':{1:138,2:120,3:112,4:94,5:86,6:78},
      'IV':{1:138,2:120,3:112,4:94,5:86,6:78}
      }

      period=1 # arbitrary here - maybe ask what moving average you want at the start?
      try:
       fd=open(dogname +"-data.csv","r")
       fd2=open("ratings.out.csv","a")
       fd3=open("calctime-mvavg.out.csv","a")
      except:
       pass
      
      dat=fd.readlines()
      data=[]
      data_calctime=[]
      for line in dat:
	 splitline=line.split()
	 if len(splitline) == 7:
	  pos=splitline[3]
	  grade=splitline[5]
	  pos=pos[:-2]
      	  pos=int(pos)
	  calt=splitline[6]
	  calctime = float(calt)
	  rat=ratings[grade][pos]
      	  if calctime != 0:
      	    data_calctime.append(calctime)
      	  if int(rat) != 0:
      	    data.append(rat)

      klist=list(movingaverage(data,period))
      klist2=list(movingaverage(data_calctime,period))
      v=(dogname,klist)
      v2=(dogname,klist2)
      value=str(v)
      value=value.replace("('","")
      value=value.replace("])","")
      value=value.replace("([","")
      value=value.replace("[","")
      value=value.replace("'","")
      value2=str(v2)
      value2=value2.replace("('","")
      value2=value2.replace("])","")
      value2=value2.replace("([","")
      value2=value2.replace("[","")
      value2=value2.replace("'","")
      fd2.write(value)
      fd3.write(value2)
      fd2.write("\n")
      fd3.write("\n")
      fd2.close()
      fd3.close()
      
def generate_html_graph():
      ''' prints moving average data to html file thats viewed in a browser '''
      try:
         txt=open("./header","r").read()
         txt2=open("./footer.ratings","r").read()
         txt3=open("./footer.time","r").read()
         fd=open("./ratings-graph.html","w")
         fd1=open("./calctime-graph.html","w")
      except:
         print "issues opening files\n"

      fd.write(txt)
      fd1.write(txt)


      dogdat=[]
      text=open("ratings.out.csv","r").readlines()
      text1=open("calctime-mvavg.out.csv","r").readlines()
      count=0
      for line in text:
      	count+=1
	line=re.sub("\'|\(|\[|\]|\)|\,","",line)
	dogdat.append(line.split())
      st1="['race #',"
      fd.write(st1)
      for line in xrange(count):
	st2="'" +dogdat[line][0] +"',"
	fd.write(st2)
      fd.write( "],")
      line=0
      for i in xrange(1,7):
       st3=" ['" +str(i)+"'," +dogdat[line][i] +","+ dogdat[line+1][i] +","+dogdat[line+2][i]+","+dogdat[line+3][i]+","+dogdat[line+4][i]+","+dogdat[line+5][i]+",] "
       fd.write(st3) 
       if i<=6:
        fd.write( ",")
       else:
        fd.write( "]);")
      fd.write(txt2)
      fd.close()

      dogdat=[]
      text=open("calctime-mvavg.out.csv","r").readlines()
      count=0
      for line in text:
      	count+=1
	line=re.sub("\'|\(|\[|\]|\)|\,","",line)
	dogdat.append(line.split())
      st1="['race #',"
      fd1.write(st1)
      for line in xrange(count):
	st2="'" +dogdat[line][0] +"',"
	fd1.write(st2)
      fd1.write( "],")
      line=0
      for i in xrange(1,7):
       try:
        st3=" ['" +str(i)+"'," +dogdat[line][i] +","+ dogdat[line+1][i] +","+dogdat[line+2][i]+","+dogdat[line+3][i]+","+dogdat[line+4][i]+","+dogdat[line+5][i]+",] "
       except:
        pass
       fd1.write(st3) 
       if i<=6:
        fd1.write( ",")
       else:
        fd1.write( "]);")
      fd1.write(txt3)
      fd1.close()




''' add a check to see if file exists, then remove if it does, else it'll error here '''
if os.path.exists("./ratings.out.csv"):
 os.remove("ratings.out.csv")
if os.path.exists("./calctime-mvavg.out.csv"):
 os.remove("calctime-mvavg.out.csv")

getdognames()
#generate_html_graph()
