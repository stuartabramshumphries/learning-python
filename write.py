#!/usr/bin/python

''' this program writes the moving averages to google chart format to display in browser '''

try:
	txt=open("./header","r").read()
	txt2=open("./footer","r").read()
	fd=open("./data.out","w")
except:
	print "issues opening files\n"

fd.write(txt)
fd.write("['race #', 'Bangcrashwallop', 'Ballymac Barn'], ['1',  160.75, 142.25], ['2',  170,   154.25], ['3',  165.5, 149.5], ['4',  156.25, 121.5], ['5',  , 121.5] ")
fd.write(txt2)

fd.close()
