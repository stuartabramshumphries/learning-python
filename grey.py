#!/usr/bin/python
import urllib
import sys
import re
import os
#import matplotlib.pyplot as plt
from movingaverage import *
from multiprocessing import Process
#from Tkinter import *
#import tkSimpleDialog

''' this program does a graphical way to input 6 dognames (i.e. for a race) - then saves them to the dognames.txt file for processing '''
#''' class MyDialog(tkSimpleDialog.Dialog):
#
#    def body(self, master):
#
#        Label(master, text="First Dog :").grid(row=0)
#        Label(master, text="Second Dog :").grid(row=1)
#        Label(master, text="Third Dog :").grid(row=2)
#        Label(master, text="Fourth Dog :").grid(row=3)
#        Label(master, text="Fifth Dog :").grid(row=4)
#        Label(master, text="Sixth Dog :").grid(row=5)
#
#        self.e1 = Entry(master)
#        self.e2 = Entry(master)
#        self.e3 = Entry(master)
#        self.e4 = Entry(master)
#        self.e5 = Entry(master)
#        self.e6 = Entry(master)
#
#        self.e1.grid(row=0, column=1)
#        self.e2.grid(row=1, column=1)
#        self.e3.grid(row=2, column=1)
#        self.e4.grid(row=3, column=1)
#        self.e5.grid(row=4, column=1)
#        self.e6.grid(row=5, column=1)
#        return self.e1 # initial focus
#
#i    def apply(self):
#        first = self.e1.get()
#        second = self.e2.get()
#        third = self.e3.get()
#        fourth = self.e4.get()
#        fifth = self.e5.get()
#        sixth = self.e6.get()
#        '''fd=open("dognames.txt","w")
#
#	for name in first,second,third,fourth,fifth,sixth:
#         fd.write(name)
#         fd.write("\n")
# 	fd.close() '''
# 
#'''

dognames="./dognames.txt"
#root=Tk()
#d = MyDialog(root)


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
      
      period=2 # arbitrary here - maybe ask what moving average you want at the start?
      try:
       fd=open(dogname +"-data.txt","r")
      except:
       print "cant open the file"
      
      dat=fd.readlines()
      data=[]
      
      for line in dat:
	splitline=line.split()
      	num=float(splitline[-1])
      	if int(num) != 0:
      	  data.append(num)

      klist=list(movingaverage(data,period))
      print "\nyo bitch, heres the moving averages \n"
      print klist
      #print_graph(klist,dogname) 
      #print_graph(data,period,dogname)
      
#def print_graph(klist,dogname):
#      ''' prints moving average data '''
#      #plt.plot(klist1,'ro',klist2,'bs',klist3,'g^',klist4,'c+',klist5,'mx',klist6,'yd')
#      plt.title('racehist')
#      plt.xlabel('number of races')
#      plt.ylabel('moving average of dogs position')
#      plt.plot(klist,label=dogname)
#      plt.legend()


getdognames()
#plt.show()



