#!/usr/bin/python

str='<td align="center" valign="middle" style="white-space:nowrap;">29/05/2013</td><td align="center" style="white-space:nowrap;">462m</td><td align="center" style="white-space:nowrap;">1</td><td align="center" style="white-space:nowrap;">5.54</td><td align="center" style="white-space:nowrap;">5th</td><td align="center" style="white-space:nowrap;">7 1/2</td><td align="left" style="white-space:nowrap;">Subway Lorraine</td><td align="left" style="white-space:nowrap;">Yarmouth</td><td align="left" style="white-space:nowrap;">RlsCrd1&3</td><td align="left" style="white-space:nowrap;">28.35</td><td align="center" style="white-space:nowrap;">N</td><td align="left" style="white-space:nowrap;">5/2</td><td align="center" style="white-space:nowrap;">A1</td><td align="center" style="white-space:nowrap;">28.92</td><td style="font-size:9pt;"><a href="resultsRace.aspx?raceID=274409-6">View Race</a></td><td style="font-size:9pt;"><a href="resultsMeeting.aspx?racedate=29/05/2013 00:00:00&amp;track=Yarmouth">View Meeting</a></td>'


nstr=str.replace('<td align="center" valign="middle" ','')
ostr=nstr.replace('<td align="center" ','')
pstr=ostr.replace('<td align="left" ','')
nnstr=pstr.replace('style="white-space:nowrap;">','"')
npstr=nnstr.replace('</td>','" ')
npstr=npstr.split('<td style=')[0]

print npstr
