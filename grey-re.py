#!/usr/bin/python
import re
def getdat():
	filedogname2='data.txt'
	fd2=open(filedogname2,"r")
	data=fd2.readlines()
	# enumerate starts at line 0
	for i,line in enumerate(data):
		 if '<td class="RCelement"><a href="res_race_result.php?raceid=' in line:
		   line=line.replace('<td class="RCelement"><a href="res_race_result.php?raceid=','')		   
		   line=line.replace('</a></td>','')
		   line=re.sub(r"^.*\>",'',line)
                   print line,
		 elif i == 2 or (i-2) % 16 == 0:
		   line=line.replace('<td class="RCelement">','')
		   line=re.sub(r"</td>$",'',line)
		   print line,
		 elif i == 4 or (i-4) % 16 ==0:
		   line=line.replace('<td class="RCelement">','')
		   line=re.sub(r"</td>$",'',line)
		   print line,
		 elif i == 5 or (i-5) % 16 == 0:
		  line=line.replace('<td class="RCelement">','')
		  line=re.sub(r"</td>$",'',line)
		  print line,
		 elif i== 10 or (i-10) % 16 ==0:
		  line=line.replace('<td class="RCelement">','')
		  line=re.sub(r"</td>$",'',line)
		  print line,
		 elif i == 13 or (i - 13) % 16 ==0:
		  line=line.replace('<td class="RCelement">','')
		  line=re.sub(r"</td>$",'',line)
		  print line,
		 elif i == 14 or (i - 14) % 16 ==0:
		  line=line.replace('<td class="RCelement">','')
		  line=re.sub(r"</td>$",'',line)
		  print line

getdat()
