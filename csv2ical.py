import csv
from datetime import datetime as dt
from datetime import date, timedelta

def date_range(start, stop, step = timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step


ical = """BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:test
X-WR-TIMEZONE:Asia/Tokyo
BEGIN:VTIMEZONE
TZID:Asia/Tokyo
X-LIC-LOCATION:Asia/Tokyo
BEGIN:STANDARD
TZOFFSETFROM:+0900
TZOFFSETTO:+0900
TZNAME:JST
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE
%s
END:VCALENDAR
"""

context = """BEGIN:VEVENT
DTSTART;TZID=Asia/Tokyo:%s
DTEND;TZID=Asia/Tokyo:%s
RRULE:FREQ=WEEKLY;WKST=MO;UNTIL=%s;BYDAY=%s
EXDATE;TZID=Asia/Tokyo:%s
STATUS:CONFIRMED
SUMMARY:%s
TRANSP:TRANSPARENT
END:VEVENT
"""

dow={'月':'MO','火':'TU','水':'WE','木':'TH','金':'FR','土':'ST','日':'SU'}
begin=['','0920','1020','1120','1300','1400','1500','1600','1700','1800']
end=['','1010','1110','1210','1350','1450','1550','1650','1750','1850']


ex=[]
with open('ex.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        st= dt.strptime (row[0],'%Y%m%d')
        ed= dt.strptime (row[1],'%Y%m%d')+timedelta(1)
        for d in date_range(st,ed):
            ex.append(d)

ctx=''
with open('import.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        title = row[0]
        aaa = dow[row[1]]
        sttime = row[4] + 'T' + begin[int(row[2])]+'00'
        edtime = row[4] + 'T' + end[int(row[3])]+'00'
        until = row[5] + 'T235959'

        extime=''
        for e in ex:
            extime += e.strftime('%Y%m%d')+ 'T'+ begin[int(row[2])]+'00,'
        ctx = ctx+context % (sttime,edtime,until,aaa,extime,title)
    print (ical % (ctx))

#print (ical % (context % (sttime,edtime,aaa,extime,title)))