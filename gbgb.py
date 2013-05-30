#!/usr/bin/python
import urllib
import sys
import re
import os
from movingaverage import *
from multiprocessing import Process

dognames="./dognames.txt"

def getdognames():
	''' this function reads a list of dognames from file '''
	dogname=open(dognames,"r").readlines()
	count=0
	for n in dogname:
		count+=1
		print n
		readdogs(n)
	if count >6:
		print "number of dogs is ",count
		print "currently only working on 6 dogs, will change in future!"
		print "exiting - delete a dog from dognames.txt"
		exit()

def readdogs(dogname):
	'''  this function reads the primary web page for eachdog '''
	dogname=dogname.replace(" ","%20")
	f=urllib.urlopen("http://www.gbgb.org.uk/raceCard.aspx?dogName="+dogname)
	ddogname=dogname.rstrip()+".txt"
	webout=open(ddogname,"w")
	s=f.read()
	webout.write(s)
	f.close()
	webout.close()
	extractdata(ddogname,dogname)
	#os.remove(ddogname)

def extractdata(filedogname,dogname):
	'''  what this function does is to format the downloaded history - basically get rid of the extraneous html '''
	dogname=dogname.rstrip()
	flag = 1
	fd=open(filedogname,"r")	
	filedogname2=dogname + "-rh.txt"
	fd2=open(filedogname2,"w")	
	data=fd.readlines()
	for line in data:
 	  #if '<td class="RCelement"><a href="' in line:
 	  if '<td align="center"' in line:
 	   fd2.write(line)
 	   flag = 0
 	  if re.search('\s+\<\/tbody\>',line): 
 	   flag = 1
	  if re.search('\s+\<\/tr\>\<tr class="Grid',line):
	   flag = 1
 	  if not flag and not '<td align="center"' in line:
 	   fd2.write(line)


	fd.close()
	os.remove(filedogname)
	fd2.close()
	analyse_data(dogname)

def analyse_data(dogname): 
	'''  this function extracts the dog data we want from its history '''
	count=0
	fd=open(dogname +"-data.txt","w")
	fd3=open(dogname + "-rh.txt","r+")
	data=fd3.readlines()
	fd3.close()
	for i,line in enumerate(data):
		nstr=line.replace('<td align="center" valign="middle" ','')
		ostr=nstr.replace('<td align="center" ','')
		pstr=ostr.replace('<td align="left" ','')
		nnstr=pstr.replace('style="white-space:nowrap;">','"')
		npstr=nnstr.replace('</td>','" ')
		npstr=npstr.split('<td style=')[0]
		spltdata=npstr.split('"')
		if len(spltdata) >10:
		 if spltdata[27] == '&nbsp;':
		  spltdata[27]='0'
		 strg=spltdata[1]+" "+spltdata[3]+" "+spltdata[9]+" "+spltdata[25]+" "+spltdata[27]
		 strg2=strg.replace('"','')
		 fd.write( strg2 )
		 fd.write( "\n" )
		
	
	fd.close()
	calc_moving_average(dogname)
	os.remove(dogname + "-rh.txt")
	 




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
      'D1':{1:133,2:118,3:106,4:95,5:85,6:71},
      'E1':{1:118,2:103,3:91,4:82,5:69,6:58},
      'H3':{1:118,2:103,3:91,4:82,5:69,6:58},
      'P3':{1:99,2:86,3:77,4:66,5:53,6:42},
      'P4':{1:99,2:86,3:77,4:66,5:53,6:42},
      'P6':{1:90,2:80,3:70,4:60,5:50,6:40},
      'IV':{1:170,2:152,3:143,4:133,5:122,6:106},
      'IT':{1:170,2:152,3:143,4:133,5:122,6:106},
      'OR':{1:170,2:152,3:143,4:133,5:122,6:106}
      }
      period=3 # arbitrary here - maybe ask what moving average you want at the start?
      try:
       fd=open(dogname +"-data.txt","r")
       fd2=open("ratings.out.txt","a")
       fd3=open("calctime-mvavg.out.txt","a")
      except:
     	pass 
      dat=fd.readlines()
      data=[]
      data_calctime=[]
      for line in dat:
	 splitline=line.split()
	 if len(splitline) == 5:
	  pos=splitline[2]
	  grade=splitline[3]
	  pos=pos[:-2]
      	  pos=int(pos)
	  calt=splitline[4]
	  calctime = float(calt)
	  rat=ratings[grade][pos]
      	  if calctime != 0:
      	    data_calctime.append(calctime)
      	  if int(rat) != 0:
      	    data.append(rat)

      klist=list(movingaverage(data,period))
      klist2=list(movingaverage(data_calctime,period))
      dogname=dogname.replace('%20','+')
      v=(dogname,klist)
      v2=(dogname,klist2)
      value=str(v)
      value2=str(v2)
      fd2.write(value)
      fd3.write(value2)
      fd2.write("\n")
      fd3.write("\n")
      fd2.close()
      fd3.close()
      
def generate_html_graph():
      ''' prints moving average data to html file thats viewed in a browser
          the basic way I've written this need at least 6 races for 6 dogs, else fails'''
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
      text=open("ratings.out.txt","r").readlines()
      text1=open("calctime-mvavg.out.txt","r").readlines()
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
      text=open("calctime-mvavg.out.txt","r").readlines()
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

if os.path.exists("./ratings.out.txt"):
 os.remove("ratings.out.txt")

if os.path.exists("./calctime-mvavg.out.txt"):
 os.remove("calctime-mvavg.out.txt")

getdognames()
generate_html_graph()
