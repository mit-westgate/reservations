#!/usr/bin/python

import cgitb;cgitb.enable()
import sys,os
sys.path.append(os.pardir)

import re,time,pytz,math,calendar,cgi,atom,smtplib
# commenting out so debugging works
import ldap
from datetime import datetime,timedelta

# these are no longer supported by google
# import gdata.calendar.service
# import gdata.calendar

from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build

# import logging
# logging.basicConfig(filename='lib.log',level=logging.DEBUG)

# updated 2018-05-25 by Yasushi
officers = {'President':'palomagr', \
            'Secretary-Treasurer':'brij', \
            'Parents Resource Coordinator':'eldante', \
            'Couples Resource Coordinator':'galashin', \
            'Partners Community Coordinator':'ivanko', \
            'Information & Technology Coordinator':'yasushis', \
            'Sustainability Coordinator':'elehnhar', \
            'Community Coordinator':'yyn', \
            'Social Chair':'noyman', \
            'Residental Life Associate':'naomic'}

superusers = {'President':'palomagr', \
             'Secretary-Treasurer':'brij', \
             'Information & Technology Coordinator':'yasushis', \
             'Residental Life Associate':'naomic'}

lngcal = 'http://www.google.com/calendar/embed?src=jbt1onapg3ffroh27umi9qm4ic%40group.calendar.google.com'
bbqcal = 'http://www.google.com/calendar/embed?src=tjsllo1pojk4tpcp40l8pinseg%40group.calendar.google.com'
eventreg = 'http://web.mit.edu/westgate/documents/MIT Event Registration Form.pdf'
alcreg = 'http://web.mit.edu/westgate/documents/Westgate Alcohol Registration Form.pdf'
alcpolicy = 'http://web.mit.edu/alcohol/www/index.html'

main = 'http://westgate.mit.edu'
# main = 'http://westgate.scripts.mit.edu'
# root = 'https://westgate.mit.edu:444/scripts/reservations/'
root = 'https://westgate.scripts.mit.edu:444/scripts/reservations/'
css = root+'style.css'
form = root+'form.py'
process = root+'process.py'
confirm = root+'confirm.py'
admin = root+'admin.py'
table = root+'table.py'
payment = root+'payment.py'
credit = root+'credit.py'
lngrule = root+'lounge.py'
bbqrule = root+'barbecue.py'

test_0612 = root+'test_0612.py'

user = 'westgate.gc@gmail.com'
password = 'joseph'

admin_name = 'Information and Publicity Coordinator'
admin_email = 'westgate-ipc@mit.edu'
# admin_apt = '1608'
admin_map_url = 'http://maps.google.com/maps?q=42.354987,-71.103922&num=1&t=h&'\
            'sll=42.354002,-71.103732&sspn=0.006295,0.006295&ie=UTF8&'\
            'll=42.35521,-71.103548&spn=0.001483,0.003484&z=19'

money_collect_name = 'Secretary-Treasurer'
money_collect_email = 'westgate-sec-treas@mit.edu'
money_collect_room = '1608'

emailsender = admin_email
nfree = 6

db = os.curdir+os.sep+'db'+os.sep
freedb = db+'free.txt'

noauth = \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>No Authorization</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    No Authorization
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
   </h3>
   <hr>
   This page is only accessible to certain members of the Westgate
   Executive Committee and the Westgate House Team with MIT
   certificates.
  </div>
 </body>
</html>
""" % {'css':css,'form':form,'main':main}

names = ['Lounge','Barbecue']
areas = ['Westgate Lounge Reservations','Westgate BBQ Reservations']
advance = 30
blackout = [(5,0,-1),(7,4),(9,0,0)]
costperblk = 10
timeperblk = 4

#----------------------------------------------------------------------------------
def Uid2Office(uid):
    global officers
    office = [v for v,k in officers.items() if k.split(',').count(uid)]
    if len(office) == 1:
        return office[0]
    else:
        return None

#----------------------------------------------------------------------------------
def Redirect(url):
    print 'Content-type: text/html'
    print
    print \
"""
<html>
 <head>
  <meta http-equiv="refresh" content="0; url=%s">
 </head>
 <body>
 </body>
</html>
""" % url

#----------------------------------------------------------------------------------
def IsSecure():
    e = os.environ
#    return e.has_key('HTTPS') and e['HTTPS'] == 'on' and e['HTTP_HOST'] == 'westgate.mit.edu:444'
    return e.has_key('HTTPS') and e['HTTPS'] == 'on' and e['HTTP_HOST'] == 'westgate.scripts.mit.edu:444'

#----------------------------------------------------------------------------------
def SecureRedirect():
    e = os.environ
    Redirect('https://'+'westgate.scripts.mit.edu:444'+e['REQUEST_URI'])
#    Redirect('https://'+'westgate.mit.edu:444'+e['REQUEST_URI'])

#-------------------------------------------------------------------------------
def Dt2Tz(dt):
    #dt is date in the form: %04d-%02d-%02d%(y,m,d)
    if(bool(pytz.timezone('US/Eastern').dst(datetime.strptime(dt,'%Y-%m-%d')))):
      return '-04:00';
    else:
      return '-05:00';
    
#----------------------------------------------------------------------------------
def Tz2Dt():
    tz = time.strftime('%z')
    s = int(tz[0]+str(int(tz[1:3])*3600+int(tz[3:])))
    return timedelta(0,s)

#----------------------------------------------------------------------------------
# This function returns the time zone as a string formatted "-HH:MM". For instance,
# East Coast time returns "-04:00".

def Tz2Str():
    tz = time.strftime('%z')
    return '%s%02d:%s' % (tz[0],int(tz[1:3]),tz[3:])

#----------------------------------------------------------------------------------
def Goog2Dt(s):
    f2 = '%Y-%m-%dT%H:%M:%S.000'
    f1 = u'%Y-%m-%dT%H:%M:%S'
    try:
        return datetime(*(time.strptime(s[:-6],f1)[:6]))
    except: 
        return datetime(*(time.strptime(s[:-6],f2)[:6]))

#----------------------------------------------------------------------------------
def Dt2Goog(d,mittz=Tz2Str()):
    f = '%Y-%m-%dT%H:%M:%S.000'
    if d.year < 1900:
        d = datetime(1900,1,1,0,0)
    return datetime.strftime(d,f)+mittz
   #return datetime.strftime(d,f)+Tz2Str()

#----------------------------------------------------------------------------------
def Goog2Str(d):
    if isinstance(d, dict) and d.has_key('dateTime'):
        d=d['dateTime'].encode('ascii','ignore')
    elif isinstance(d, basestring):
        d=d.encode('ascii','ignore')
    else:
        return ""

    f = '^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})T(?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})(?P<sgn>[+-])(?P<oH>\d{2}):(?P<oM>\d{2})$'
    expr = re.compile(f)
    match = expr.match(d)
    if match == None:
        f = '^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})(?:T(?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})\.(?P<MS>\d{3})(?:Z|(?P<sgn>[+-])(?P<oH>\d{2}):(?P<oM>\d{2})))?$'
        expr = re.compile(f)
        match = expr.match(d)
        
    y = int(match.group('y'))
    m = int(match.group('m'))
    d = int(match.group('d'))
    H = match.group('H')
    M = match.group('M')
    S = match.group('S')
    # MS = match.group('MS')
    MS = 0
    oH = match.group('oH')
    oM = match.group('oM')
    if H == None:
        H = 0
        M = 0
        S = 0
        MS = 0
    else:
        H = int(H)
        M = int(M)
        S = int(S)
        MS = int(MS)
    dt = datetime(y,m,d,H,M,S,MS*1000)
    if oH == None:
        dt += Tz2Dt()
        return Goog2Str(Dt2Goog(dt))
    if H == 0 or H == 24:
        H = 12
        p = 'am'
    elif H == 12:
        p = 'pm'
    elif H > 12:
        H -= 12
        p = 'pm'
    else:
        p = 'am'
    days = {0:'Sun',1:'Mon',2:'Tues',3:'Wed',4:'Thurs',5:'Fri',6:'Sat'}
    wd = days[int(dt.strftime('%w'))]

    return ' %s %s-%s-%s %s:%02d%s' % (wd,m,d,y,H,M,p)

#----------------------------------------------------------------------------------
# This function takes a year and returns true if it is a leap year, false if not.

def IsLeap(y):
    if not y%400:
        return True
    elif not y%100:
        return False
    elif not y%4:
        return True
    else:
        return False

#----------------------------------------------------------------------------------
def Now2Goog():
    n = datetime.now()
    return Goog2Str(Dt2Goog(n))

#----------------------------------------------------------------------------------
# This function takes a year, month, and day of the month and returns true if this
# is a valid day of the year, false if not.

def TrueDates(y,m,d):
    dmax = [31,29,31,30,31,30,31,31,30,31,30,31]
    if dmax[m-1] < d:
        return False
    if m == 2 and d == 29 and not IsLeap(y):
        return False
    return True

#----------------------------------------------------------------------------------
# This function parses a string representing a date and returns a string formatted
# "yyyy-mm-dd". If the string cannot be parsed or the date is not
# possible, false is returned.

def ParseDate(s):
        if s == '':
            return ''
        expr = re.compile('^\s*(?P<n1>\d{1,4})[-/\s](?P<n2>\d{1,2})(?:[-/\s](?P<n3>\d{1,4}))?\s*$')
        match = expr.match(s)
        if not match:
            return False
        n1 = int(match.group('n1'))
        n2 = int(match.group('n2'))
        n3 = match.group('n3')
        if n3 == None:
            n3 = datetime.now().year
        else:
            n3 = int(n3)
        if n1 > 31 and n3 <= 31:
            d = n3
            m = n2
            y = n1
        else:
            d = n2
            m = n1
            y = n3
        if y < 100:
            y += 2000
        if not TrueDates(y,m,d):
            return False
        return '%04d-%02d-%02d' % (y,m,d)

#----------------------------------------------------------------------------------
# This function parses a string representing a time and returns a string formatted
# "HH:MM:SS.SSS-TZ". If the string cannot be parsed, false is returned.

def ParseTime(s,tz):
    if s == '':
        return ''
    expr = re.compile('^\s*(?P<n1>[\d]{1,2})((:|\s*)(?P<n2>[\d]{2}))?\s*((?P<n3>[aApP])\s*\.?\s*[mM]\s*\.?\s*)?$')
    match = expr.match(s)
    if not match:
        return False
    h = int(match.group('n1'))
    m = match.group('n2')
    if m == None:
        m = 0
    else:
        m = int(m)
    t = match.group('n3')
    if t == None:
        t = 'a'
    t = t.lower()
    if h < 0 or h > 24 or m < 0 or m > 59 or (h == 24 and m > 0):
        return False
    if h < 12 and t == 'p':
        h += 12
    if h == 12 and t == 'a' or h == 24:
        h = 0
    return '%02d:%02d:00.000%s' % (h,m,tz)

#----------------------------------------------------------------------------------
def IsMidnight(s):
    t = Goog2Dt(s)
    return t.hour+t.minute == 0

#----------------------------------------------------------------------------------
#mittz added, 
def AddDay(s,mittz):
    return Dt2Goog(Goog2Dt(s)+timedelta(1),mittz)

#----------------------------------------------------------------------------------
def InPast(s):
    return Goog2Dt(s) < datetime.now()

#----------------------------------------------------------------------------------
def InFuture(s):
    global advance
    future = datetime.now()+timedelta(advance)
    return Goog2Dt(s) > future

#----------------------------------------------------------------------------------
def Week2Date(y,m,wd,n):
    wd0,ndays = calendar.monthrange(y,m)
    return (m,range((wd-wd0)%7,ndays,7)[n]+1)

#----------------------------------------------------------------------------------
def IsBlack(s):
    global blackout
    expr = re.compile('(.*)-(.*)-(.*)T')
    y,m,d = map(int,expr.match(s).groups())
    for r in blackout:
        if len(r) == 2:
            if r == (m,d):
                return True
        else:
            if Week2Date(y,*r) == (m,d):
                return True
    return False

#----------------------------------------------------------------------------------
def Get(variable,form,default=''):
    try:
        return form.getlist(variable)[0].strip()
    except:
        return default

#----------------------------------------------------------------------------------
def CalcCost(start,end):
    global costperblk,timeperblk
    dt = Goog2Dt(end)-Goog2Dt(start)
    dth = dt.days*24.+dt.seconds/3600.+dt.microseconds/360000000.
    if dth <= 0:
        return False
    cost = int(math.ceil(costperblk*math.ceil(dth/float(timeperblk))))
    return cost,int(round(dth))

#----------------------------------------------------------------------------------
def LoginCal(cname):

    client_email = '117593083049-h1pupclppqu21eepcskepfabsu2ghh15@developer.gserviceaccount.com'
    private_key_file = 'ReservationSystem.p12'
    with open(private_key_file) as f:
      private_key = f.read()
    credentials = SignedJwtAssertionCredentials(client_email, private_key,
        'https://www.googleapis.com/auth/calendar')

    http_auth = credentials.authorize(Http())
    service = build('calendar', 'v3',http=http_auth)

    lounge_id = 'jbt1onapg3ffroh27umi9qm4ic@group.calendar.google.com'
    bbq_id = 'tjsllo1pojk4tpcp40l8pinseg@group.calendar.google.com'

    global areas
    if cname == areas[0]:
        return service, lounge_id
    if cname == areas[1]:
        return service, bbq_id
    return None, None

    """
    global user,password
    cs = gdata.calendar.service.CalendarService()
    cs.email = user
    cs.password = password
    cs.source = 'Google-Calendar_Python_Sample-1.0'
    cs.ProgrammaticLogin()
    feed = cs.GetCalendarListFeed()
    url = ''
    for entry in feed.entry:
        if entry.title.text == cname:
            url = entry.link[0].href
            break
    if url == '':
        return False
    return cs,url
    """

#----------------------------------------------------------------------------------
def DateQuery(cs,url,start,end):
    request = cs.events().list(calendarId=url, timeMin=start, timeMax=end, maxResults=100)
    response = request.execute()
    return [elem for elem in response.get('items', []) if elem['status'] != 'cancelled']
    """
    expr = re.compile('http://www\.google\.com/calendar/feeds/([^/]*)/private/full')
    match = expr.match(url)
    if match == None:
        return None
    userid = match.groups()[0]
    userid = userid.replace('%40','@')
    #this is where there is an issue. userid isn't correct?
    query = gdata.calendar.service.CalendarEventQuery(userid,'private','full')
    query.start_min = start
    query.start_max = end
    query.max_results = '100'
    return cs.CalendarQuery(query)
    """

def DeleteEvent(cs, url, event):
    request = cs.events().delete(calendarId=url, eventId=event['id'])
    request.execute()
    """
    cs.Delete(event.GetEditLink().href)
    """

#----------------------------------------------------------------------------------
def UpdateEvent(cs, url, event):
    request = cs.events().update(calendarId=url, eventId=event['id'], body=event)
    request.execute()
    """
    cs.Delete(event.GetEditLink().href)
    """

#----------------------------------------------------------------------------------
def EventExists(event):
    return len(event['start']) > 0 and event['status'] != 'CANCELED'
    """
    return len(event.when) > 0 and event.event_status.value != 'CANCELED'
    """

#----------------------------------------------------------------------------------
def KeepEvent(event,paid,unpaid):
    items = RetrieveItems(event)
    pay = items.get('wg_pay','') == 'True'
    return EventExists(event) and (pay and paid) or (not pay and unpaid)

#----------------------------------------------------------------------------------
def IsConflict(cs,url,start,end):
    feed = DateQuery(cs,url,start,end)
    for event in feed:
        if EventExists(event):
            return True
    """
    if len(feed.entry) == 0:
        return False
    for event in feed.entry:
        if EventExists(event):
            return True
    """
    return False

#----------------------------------------------------------------------------------
def CalContent(p):
    if p['wec']:
        official = 'This is an official Westgate event'
        paystr = 'Fee waived'
    else:
        official = 'This is a private event'
        if p['free']:
            paystr = 'Fee waived'
        elif p['pay'] == 'True':
            paystr = 'Received'
        else:
            paystr = 'Not received'
    startstr = Goog2Str(p['start'])
    endstr = Goog2Str(p['end'])
    sizestr = (p['size'] == 'large')* \
              ('\nThere will be 100 or more guests at this event and I '+ \
               'will file all necessary forms and comply with all '+ \
               'policies found on the MIT Event Registration Form at '+ \
               'http://web.mit.edu/westgate/documents/'+
               'MIT%20Event%20Registration%20Form.pdf.\n')
    alcstr = (p['alc'] == 'yessmall')* \
             ('\nAlcohol will be at this event and there will be 50 or '+ \
              'fewer guests. I will file all necessary forms and comply '+ \
              'with all policies found on the Westgate Alcohol '+ \
              'Registration Form at http://web.mit.edu/westgate/documents/'+ \
              'Westgate%20Alcohol%20Registration%20Form.pdf.\n')+ \
              (p['alc'] == 'yeslarge')* \
              ('\nAlcohol will be at this event and there will be more '+ \
               'than 50 guests. I will file all necessary forms and comply '+ \
               'with all policies found at Alcohol Policies and Procedures '+ \
               '@ MIT at http://web.mit.edu/alcohol/www/index.html and '+ \
               'on the MIT Event Registration Form at http://web.mit.edu'+ \
               '/westgate/documents/MIT%20Event%20Registration%20Form.pdf.\n')
    p.update({'official':official,'paystr':paystr,'startstr':startstr, \
              'endstr':endstr,'sizestr':sizestr,'alcstr':alcstr})
    private = \
"""
%(official)s
Payment status: %(paystr)s
Payment amount: $%(cost)s
Name: %(name)s
Apartment: %(apt)s
Daytime phone: %(dfone)s
Evening phone: %(efone)s
E-mail address: %(email)s
Event title: %(etitle)s
Event start: %(startstr)s
Event end: %(endstr)s
%(sizestr)s%(alcstr)s""" % p
    public = \
"""
%(official)s
Payment status: %(paystr)s
Payment amount: $%(cost)s
Event title: %(etitle)s
Event start: %(startstr)s
Event end: %(endstr)s
""" % p
    return private,public

#----------------------------------------------------------------------------------
def File2Param(fn,t):
    try:
        f = open(fn,'r')
        p = eval(f.read())
        f.close()
        if t=='l':
            return list(p)
        elif t=='d':
            return dict(p)
        else:
            return str(p)
    except:
        if t=='l':
            return []
        elif t=='d':
            return {}
        else:
            return ''

#----------------------------------------------------------------------------------
def Param2File(p,fn):
    f = open(fn,'w')
    f.write(str(p))
    f.close()

#----------------------------------------------------------------------------------
def SortEvent(e1,e2):
    start1 = e1['start']
    start2 = e2['start']
    return cmp(start2,start1)

#----------------------------------------------------------------------------------
def InsertEvent(cs,url,title,content,where,start,end,items):
    event = {}
    event['summary']= title
    event['description'] = content
    event['location']=where
    startDateTime = {}
    startDateTime['dateTime']=start
    event['start']=startDateTime
    endDateTime = {}
    endDateTime['dateTime']=end
    event['end']=endDateTime
    shared = {}
    for key,val in items.items():
        shared[key]=val
    extendedProperties = {}
    extendedProperties['shared'] = shared
    event['extendedProperties'] = extendedProperties
    request = cs.events().insert(calendarId=url, body=event)
    response = request.execute()
    return response

#----------------------------------------------------------------------------------
def RetrieveItems(event):
    d = {}
    if not(event.has_key('extendedProperties')):
        return d
    if not(event['extendedProperties'].has_key('shared')):
        return d
    for shared_property in (event['extendedProperties']['shared'].iteritems()):
       name = shared_property[0]
       value = shared_property[1]
       d[name] = value
    """
    for propprop in event.extended_property:
        d[prop.name] = prop.value
    """
    return d

#----------------------------------------------------------------------------------
def SetItems(event,items):
    for key,val in items.items():
        n = 0
        if not(event.has_key('extendedProperties')):
            event['extendedProperties'] = {}
        if event['extendedProperties'].has_key('shared'):
            n = len(event['extendedProperties']['shared'])
        else:
            event['extendedProperties']['shared'] = {}
#        flag = False
#        for i,prop in zip(range(n),event['extendedProperties']['shared']):
#            if prop.name == key:
#                event['extendedProperties']['shared'][i].value = val
#                flag = True
#                break
#        if not flag:
#            event['extendedProperties']['shared'][key]=val
        event['extendedProperties']['shared'][key]=val
    return event

#----------------------------------------------------------------------------------
def GetCredit():
    global freedb,nfree,costperblk
    uid = GetAttributes('uid')
    office = [v for v,k in officers.items() if k.split(',').count(uid)]
    if len(office) == 1:
        office = office[0]
        free = File2Param(freedb,'d')
        if not free.has_key(office):
            free[office] = nfree
            Param2File(free,freedb)
        credit = free[office]*costperblk
        return credit
    else:
        return None

#----------------------------------------------------------------------------------
def ProcessForm(form,ispay=False):
    global names,areas
    Getf = lambda x:Get(x,form)
    ntitle = Getf('ntitle')
    gname = Getf('gname')
    fname = Getf('fname')
    apt = Getf('apt')
    dfone = Getf('dfone')
    efone = Getf('efone')
    email = Getf('email')
    etitle = Getf('etitle')
    area = Getf('area')
    date = ParseDate(Getf('date'))
    mittz = Dt2Tz(date)
    tstart = Getf('tstart')
    tend = Getf('tend')
    pstart = ParseTime(tstart,mittz)
    pend = ParseTime(tend,mittz)
    wec = Getf('wec') == 'True'
    free = Getf('free') == 'True'
    agree = Getf('agree')
    size = Getf('size')
    alc = Getf('alc')
    credit = GetCredit()
    errors = []
    if wec and not (OfficerAuth() or SuperAuth()):
        errors.append('You are not authorized to request WEC-sponsored events')
    if ntitle == '':
        errors.append('You did not enter a personal title')
    if gname == '':
        errors.append('You did not enter a given name')
    if fname == '':
        errors.append('You did not enter a family name')
    if apt == '':
        errors.append('You did not enter an apartment number')
    if dfone == '':
        errors.append('You did not enter a daytime phone number')
    if efone == '':
        errors.append('You did not enter an evening phone number')
    if not ValidEmail(email):
        errors.append('You did not enter a valid e-mail address')
    if etitle == '':
        errors.append('You did not enter an event title')
    if area == '':
        errors.append('You did not choose a reservation location')
        cname = ''
        cs = ''
        url = ''
    else:
        if area == names[0]:
            cname = areas[0]
        else:
            cname = areas[1]
        cs,url = LoginCal(cname)
    if date == '':
        errors.append('You did not enter an event date')
    if date == False:
        errors.append('You improperly formatted the event date')
    if pstart == '':
        errors.append('You did not enter a starting time')
    if pstart == False:
        errors.append('You improperly formatted the starting time')
    if pend == '':
        errors.append('You did not enter an ending time')
    if pend == False:
        errors.append('You improperly formatted the ending time')
    if free and credit == None:
        errors.append('You are not authorized as a Westgate officer and cannot waive reservation fees')
    if agree == '':
        errors.append('You did not agree to the reservation rules')
    if size == '':
        errors.append('You did not indicate the size of your event')
    if alc == '':
        errors.append('You did not indicate if alcohol would or would not be present')
    if bool(date) and bool(pstart) and bool(pend):
        start = date+'T'+pstart
        end = date+'T'+pend
        if IsMidnight(end):
            end = AddDay(end,mittz)
        if start >= end:
            errors.append('The event start time is not before the event end time')
        if InPast(start):
            errors.append('The event date occurs in the past')
        if InFuture(end) and not (OfficerAuth() or SuperAuth()):
            errors.append('You can only schedule an event at most %s days in advance' % advance)
        if area == names[1] and IsBlack(start):
            errors.append('The barbecue area cannot be reserved on this date because it is a holiday. See the reservation rules for more information')
        if area != '' and IsConflict(cs,url,start,end):
            errors.append('There is another event already scheduled during your time range at your location. ');
        #bug fixed (jlmiao@mit.edu)
        #'Note there is known bug with daylight savings time. If the calendar shows a back to back event but your slot is free, try moving the event by an hour. This can fix the problem if you are scheduling an event that takes place after a switch in daylight savings time.')
        cost,dt = CalcCost(start,end)
        if free and credit != None and credit < cost:
            errors.append('You do not have sufficient officer reservation credit to waive the reservation fee')
    else:
        start = ''
        end = ''
        cost = None
        dt = None
    if wec and free and (OfficerAuth() or SuperAuth()):
        errors.append('An officer fee waiver is not required for a WEC-sponsored event.')
    if ispay:
        pay = Getf('pay') == 'True'
        if not pay:
            errors.append('You did not confirm your reservation and agree to payment')
    return {'ntitle':ntitle,'gname':gname,'fname':fname, \
            'apt':apt,'dfone':dfone,'efone':efone,'email':email, \
            'etitle':etitle,'area':area,'date':date,'tstart':tstart, \
            'tend':tend,'wec':wec,'free':free,'agree':agree, \
            'size':size,'alc':alc,'start':start,'end':end, \
            'errors':errors,'cname':cname,'cs':cs,'url':url, \
            'cost':cost,'dt':dt,'credit':credit}

#----------------------------------------------------------------------------------
# Multiple addresses in one argument must be separated by commas
def SendMail(sender='',proxy=None,to='',cc='',bcc='',subject='',text=''):
    if proxy == None:
        proxy = sender
    message = 'From: %s\nTo: %s\nCc: %s\nBcc: %s\nSubject: %s\n\n%s' % (proxy,to,cc,bcc,subject,text)
    recipients = (',').join([to,cc,bcc]).split(',')
    server = smtplib.SMTP('outgoing.mit.edu')
    try:
        server.sendmail(sender,recipients,message)
    except smtplib.SMTPRecipientsRefused:
        e = 'SMTPRecipientsRefused'
    except smtplib.SMTPHeloError:
        e = 'SMTPHeloError'
    except smtplib.SMTPSenderRefused:
        e = 'SMTPSenderRefused'
    except smtplib.SMTPDataError:
        e = 'SMTPDataError'
    except:
        e = 'Unexpected Error'
    else:
        e = None
    server.quit()
    return e

#----------------------------------------------------------------------------------
# Based on http://en.wikipedia.org/wiki/E-mail_address#Limitations
def ValidEmail(email):
    lc = "[-\w!#$%*/?|^{}`~&'+=]"
    lcd = "[-\w!#$%*/?|^{}`~&'+=.]"
    dm = '[-a-zA-Z0-9]'
    expr = re.compile("""((?:%s+%s?)*%s@(?:%s+\.)*%s+)""" % (lc,lcd,lc,dm,dm))
    m = expr.match(email)
    return bool(m) and m.end() == len(email)

#----------------------------------------------------------------------------------
# eduPersonPrimaryAffiliation   Primary affiliation status
# cn                            Full name
# uidNumber
# eduPersonScopedAffiliation
# street                        Street address
# eduPersonPrincipalName
# uid                           Athena user ID
# postalCode                    Postal code
# mail                          E-mail address
# loginShell
# gidNumber
# homePhone                     Home phone number
# apple-user-homeDirectory      Apple home directory
# l                             City
# o
# st                            State
# eduPersonAffiliation          Affiliation status
# sn                            Last name
# homeDirectory                 Athena home directory
# ou                            Department
# givenName                     First name

def GetAttributes(attr):
    try:
        keys = os.environ.keys()
        keys.sort()
        searchid = os.environ['SSL_CLIENT_S_DN_Email'].split('@')
        l = ldap.open("ldap.mit.edu")
        l.protocol_version = ldap.VERSION3
        baseDN = "dc=mit,dc=edu"
        searchScope = ldap.SCOPE_SUBTREE
        searchFilter = "uid="+searchid[0]
        retrieveAttributes = None
        ldap_result_id = l.search(baseDN,searchScope,searchFilter,retrieveAttributes)
        result_type,result_data = l.result(ldap_result_id,0)
        return result_data[0][1][attr][0]
    except:
        return False

#----------------------------------------------------------------------------------
def OfficerAuth():
    global officers
    users = ','.join(officers.values()).split(',')
    uidauth = GetAttributes('uid')
    return bool(users.count(uidauth))

#----------------------------------------------------------------------------------
def SuperAuth():
    global superusers
    users = ','.join(superusers.values()).split(',')
    uidauth = GetAttributes('uid')
    return bool(users.count(uidauth))
