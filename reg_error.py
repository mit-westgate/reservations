#!/usr/bin/python

import cgitb;cgitb.enable()
import lib,cgi
import time
import gdata.calendar.service
import gdata.calendar
import re

import logging
logging.basicConfig(filename='lib.log',level=logging.DEBUG)

def ErrorQuery(cs,url,title,author):
    expr = re.compile('http://www\.google\.com/calendar/feeds/([^/]*)/private/full')
    match = expr.match(url)
    if match == None:
        return None
    userid = match.groups()[0]
    userid = userid.replace('%40','@')
    query = gdata.calendar.service.CalendarEventQuery(userid,'private','full')
    vars(query)
    #query.start_min = start
    #query.start_max = end
    query.max_results = '100'
    return cs.CalendarQuery(query)

cname = lib.areas[0]
date = lib.ParseDate("11/8/14")
dateEnd = lib.ParseDate("11/9/14")
pstart = lib.ParseTime("12pm")
pend = lib.ParseTime("2pm")
start = date+'T'+pstart
end = dateEnd+'T'+pstart

cs,url=lib.LoginCal(cname)

print 'Content-type: text/html'
print
print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<body>
"""

print "start: "
print start
print "<br/>end: "
print end
print "<br/>cname: "
print cname
print "<br/>cs: "
print cs
print "<br/>cs type: "
print type(cs)
print "<br/>url: "
print url
print "<br/>"


if lib.IsConflict(cs,url,start,end):
    print("Conflict<br/>") 
    feed = lib.DateQuery(cs,url,start,end)
    #feed = ErrorQuery(cs,url,"WEC","drchurchill28")
    for event in feed:
        #print "<br/>"
        #print "<br/>"
        #print vars(event)
        print "<br/>"
        print event['summary']
        print "<br/>"
        print event['creator']
        print "<br/>"
        #print event.contributor[0]
        #print "<br/>"
        #print event.who[0]
        #print "<br/>"
        if len(event['start']) == 0:
            lib.DeleteEvent(cs,url, event)
            print "ERROR, no start date, event deleted"
        if str(event['summary']).find("Josh") != -1:
            lib.DeleteEvent(cs,url, event)
            print "Event found and deleted"
        #print event.when[0].end_time
        #print "<br/>"
        #print event.when[0].start_time
        #print "<br/>"
else:
    print("No Conflict")



print time.time()
print \
"""
<br/>
Done
</body>
</html>
"""

