#!/usr/bin/python
def analyse_data(dogname): 
#       '''  this function extracts the dog data we want from its history '''
        dogname="frettenham+flyer"
        filedogname2=dogname + "-rh.txt"
        print "filename is ", filedogname2
        #fd3=open(filedogname2,"r")
        fd3=open("./frettenham+flyer-rh.txt","rb")
        print fd3 
        print fd3.name
        print fd3.fileno()
        fd=open(dogname +"-data.txt","w")
        #fd3=open(dogname + "-rh.txt","r+")
        data2=fd3.readlines()
        print data2
        fd3.close
        exit()

analyse_data("fred")
