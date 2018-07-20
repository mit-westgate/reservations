#!/usr/bin/python

import cgitb;cgitb.enable()
import lib,cgi

i = -1

def GetEvent(event,area,paid,unpaid):
    global i
    i += 1
    items = lib.RetrieveItems(event)
    cost = items.get('wg_cost','0')
    name = items.get('wg_name','%(admin_name)s' % {'admin_name':lib.admin_name})
    apt = items.get('wg_apt',lib.money_collect_room)
    dfone = items.get('wg_dfone','N/A')
    efone = items.get('wg_efone','N/A')
    email = items.get('wg_email','%(admin_email)s' % {'admin_email':lib.admin_email} )
    paystr = items.get('wg_pay','False')
    wec = items.get('wg_wec','True') == 'True'
    free = items.get('wg_free','False') == 'True'
    if wec or free:
        cost = 0
    if wec:
        clss = ' wec'
    elif free:
        clss = ' free'
    else:
        clss = ''
    pay = paystr == 'True'
    start = event['start']['dateTime']
    end = event['end']['dateTime']
    reg = event.get('published',None)
    etitle = event['summary']
    startstr = lib.Goog2Str(start)
    endstr = lib.Goog2Str(end)
    regstr = lib.Goog2Str(reg)
    check = pay*' checked'
    return \
"""
<tr class="admtop">
 <td class="%(clss)s">
  <input type="checkbox" name="box%(i)s" value="True"%(check)s>
  <input type="hidden" name="start%(i)s" value="%(start)s">
  <input type="hidden" name="end%(i)s" value="%(end)s">
  <input type="hidden" name="etitle%(i)s" value="%(etitle)s">
  <input type="hidden" name="area%(i)s" value="%(area)s">
  <input type="hidden" name="pay%(i)s" value="%(paystr)s">
 </td>
 <td class="%(clss)s">
   <input type="checkbox" name="delete%(i)s" value="True">
 </td>
 <td class="%(clss)s">$%(cost)s</td>
 <td class="%(clss)s">%(name)s</td>
 <td>
  <a href="javascript:toggle('%(i)s')" class="%(clss)s">%(etitle)s</a>
 </td>
 <td class="%(clss)s">%(startstr)s</td>
</tr>
<tr id="%(i)s" style="display:none">
 <td class="notop"></td>
 <td class="notop"></td>
 <td colspan="3" class="notop%(clss)s">
  Apartment: %(apt)s<br>
  Daytime phone: %(dfone)s<br>
  Evening phone: %(efone)s<br>
  E-mail address: <a href="mailto:%(email)s" class="%(clss)s">%(email)s</a><br>
  Event end: %(endstr)s<br>
  Registered: %(regstr)s
 </td>
</tr>
""" % {'i':i,'check':check,'cost':cost,'name':name,'etitle':etitle, \
       'startstr':startstr,'apt':apt,'dfone':dfone,'efone':efone, \
       'email':email,'endstr':endstr,'start':start,'end':end, \
       'regstr':regstr,'area':area,'paystr':paystr,'clss':clss}

def GetArea(area,fstart,fend,paid,unpaid):
    cs,url = lib.LoginCal(area)
    feed = lib.DateQuery(cs,url,fstart,fend)
    # events = feed.entry
    events = feed
    events.sort(cmp=lib.SortEvent)
    events = filter(lambda x:lib.KeepEvent(x,paid,unpaid),events)
    eventhtml = ''.join([GetEvent(e,area,paid,unpaid) for e in events])
    return \
"""
<tr>
 <td colspan="5" class="area">
  <h3>%(area)s</h3>
 </td>
</tr>
<tr>
 <td class="head3">Paid</td>
 <td class="head3">Delete</td>
 <td class="head3">Cost</td>
 <td class="head3">Name</td>
 <td class="head3">Event</td>
 <td class="head3">Time</td>
</tr>
%(eventhtml)s
""" % {'area':area,'eventhtml':eventhtml}

if not lib.IsSecure():
    lib.SecureRedirect()
else:
    
    if not lib.SuperAuth():
        print 'Content-type: text/html'
        print
        print lib.noauth
    else:
        form = cgi.FieldStorage()
        Get = lambda x:lib.Get(x,form)
        dstart = lib.ParseDate(Get('dstart'))
        dend = lib.ParseDate(Get('dend'))
        unpaid = Get('unpaid') == 'True'
        paid = Get('paid') == 'True'
        errors = []
        if dstart == '':
            errors.append('You did not enter a start date')
        elif dstart == False:
            errors.append('You improperly formatted the start date')
        if dend == '':
            errors.append('You did not enter an end date')
        elif dend == False:
            errors.append('You improperly formatted the end date')
        if len(errors) > 0:
            errors = '<ul>\n<li>'+'</li>\n<li>'.join(errors)+'</li>\n</ul>'
            print 'Content-type: text/html'
            print
            print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Westgate Reservations Error</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    <p class="left">
     User Error
     &#183; <a href="%(form)s">Reservation Application</a>
     &#183; <a href="%(main)s">Westgate Home</a>
    </p>
    <p class="right">
     <a href="%(admin)s">Admin</a>
    </p>
    <div class="clear"></div>
   </h3>
   <hr>
   Your form submission generated the following errors and warnings.
   Please go back and try again.
   %(errors)s
  </div>
 </body>
</html>
""" % {'css':lib.css,'errors':errors,'main':lib.main,'form':lib.form, \
       'admin':lib.admin}
        else:
            fstart = dstart+'T00:00:00.000'+lib.Tz2Str()
            fend = dend+'T00:00:00.000'+lib.Tz2Str()
            tabhtml = u''.join([GetArea(a,fstart,fend,paid,unpaid) for a in lib.areas]).encode('utf-8').strip()
            print 'Content-type: text/html'
            print
            print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Payment Verification</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
  <script language="javascript" type="text/javascript">
   function toggle(row) {
    var e = document.getElementById(row);
    current = e.style.display;
    next = (current == 'none') ? '' : 'none';
    e.style.display = next;
   }
  </script>
 </head>
 <body>
  <div id="main">
   <h3>
    <p class="left">
     Payment Verification
     &#183; <a href="%(form)s">Reservation Application</a>
     &#183; <a href="%(main)s">Westgate Home</a>
    </p>
    <p class="right">
     <a href="%(admin)s">Admin</a>
    </p>
    <div class="clear"></div>
   </h3>
   <hr>
   Events in red are tentatively sponsored by WEC. Events in green are private
   events for officers using one of their waivers. Events in black are private
   and payment. Check boxes to approve the event and either waive the fee
   (for WEC-sponsored and officer-sponsored events) or confirm receipt of
   payment (for private events). In all cases, an e-mail will be sent to the
   event registrant. Note that a maximum of 100 reservations (paid and unpaid
   combined) are retrieved for either calendar for any given query, so for large
   date ranges not all reservations might be displayed. Use narrow date ranges to
   be certain that all reservations are displayed.
   <form method="post" action="%(payment)s">
    <input type="hidden" name="max" value="%(i)s">
    <table id="info">
      %(tabhtml)s
    </table>
    <div class="submit">
     <input type="submit" value="Submit">
    </div>
   </form>
  </div>
 </body>
</html>""" % {'css':lib.css,'tabhtml':tabhtml,'admin':lib.admin, \
       'payment':lib.payment,'i':i,'form':lib.form,'main':lib.main}
