#!/usr/bin/python

import cgitb;cgitb.enable()
import lib,cgi

def StatusHtml(e):
    status = ''
    if e['wec'] and e['pay']:
        status = \
"""The event <strong>%(etitle)s</strong> has been officially approved as a
WEC-sponsored activity. A confirmation e-mail has been sent."""
    elif e['wec'] and not e['pay']:
        status = \
"""The event <strong>%(etitle)s</strong> has <strong>not</strong> been
officially approved as a WEC-sponsored activity. A confirmation e-mail has
<strong>not</strong> been sent."""
    elif e['free'] and e['pay']:
        status = \
"""The officer fee-waiver for the event <strong>%(etitle)s</strong> has
been officially approved. A confirmation e-mail has been sent."""
    elif e['free'] and not e['pay']:
        status = \
"""The officer fee waiver for the event <strong>%(etitle)s</strong> has
<strong>not</strong> been officially approved. A confirmation e-mail has
<strong>not</strong> been sent."""
    elif e['pay']:
        status = \
"""The payment status of the event <strong>%(etitle)s</strong> has been changed
to <strong>received</strong> and a confirmation e-mail has been sent to %(name)s
at <href="mailto:%(email)s">%(email)s</a>."""
    else:
        status = \
"""The payment status of the event <strong>%(etitle)s</strong> has been changed
to <strong>not received</strong>. A confirmation e-mail has
<strong>not</strong> been sent."""
        # a bit hacky, know that this will only be called if other values are false
    if e['delete']:
        status = \
"""The event <strong>%(etitle)s</strong> has been deleted."""
    return \
"""
<tr>
 <td>
%(status)s
 </td>
</tr>
""" % {'status':(status % e)}
                    
if not lib.SuperAuth():
    print 'Content-type: text/html'
    print
    print lib.noauth
else:
    form = cgi.FieldStorage()
    Get = lambda x:lib.Get(x,form)
    nmax = int(lib.Get('max',form,default=-1))
    changed = []
    for i in range(nmax+1):
        si = str(i)
        box = Get('box'+si) == 'True'
        pay0 = Get('pay'+si) == 'True'
        delete = Get('delete'+si) == 'True'
        if box == (not pay0):
            start = Get('start'+si)
            end = Get('end'+si)
            etitle = Get('etitle'+si)
            area = Get('area'+si)
            cs,url = lib.LoginCal(area)
            feed = lib.DateQuery(cs,url,start,end)
            for event in feed:
                if event['summary'] == etitle:
                    items = lib.RetrieveItems(event)
                    cost = items.get('wg_cost','?')
                    name = items.get('wg_name','?')
                    apt = items.get('wg_apt','?')
                    dfone = items.get('wg_dfone','?')
                    efone = items.get('wg_efone','?')
                    email = items.get('wg_email','?')
                    wec = items.get('wg_wec','?') == 'True'
                    free = items.get('wg_free','?') == 'True'
                    size = items.get('wg_size','?')
                    alc = items.get('wg_alc','?')
                    start = event['start']['dateTime']
                    end = event['end']['dateTime']
                    paystr = str(box)
                    event = lib.SetItems(event,{'wg_pay':paystr})
                    content = {'name':name,'cost':cost,'apt':apt, \
                               'dfone':dfone,'efone':efone,'email':email, \
                               'wec':wec,'pay':paystr,'size':size, \
                               'alc':alc,'etitle':etitle,'start':start, \
                               'end':end,'free':free}
                    private,public = lib.CalContent(content)
                    if not name == '?':
                        event['description'] = public
                    lib.UpdateEvent(cs, url, event)
                    areastr = (lib.areas[0] == area)*'Lounge'+ \
                              (lib.areas[0] != area)*'Barbecue'+' Reservation'
                    if box:
                        if wec:
                            text = \
"""
Your event has been officially approved as a WEC-sponsored activity.
%(private)s""" % {'private':private}
                        elif free:
                            credit = max(0,lib.GetCredit())
                            text = \
"""
As a Westgate officer, your fee of $%(cost)s for your event has been waived.
You have $%(credit)s of credit remaining.
%(private)s""" % {'cost':cost,'credit':credit,'private':private}
                        else:
                            text = \
"""
The payment of $%(cost)s for your event has been received.
%(private)s""" % {'cost':cost,'private':private}
                        sender = lib.emailsender
                        proxy = '"%(admin_name)s" <%(admin_email)s>' %{'admin_email':lib.admin_email,'admin_name':lib.admin_name}
                        to = '"%(name)s" <%(email)s>' % {'name':name,'email':email}
                        bcc = '"%(admin_name)s" <%(admin_email)s>' %{'admin_email':lib.admin_email,'admin_name':lib.admin_name}
                        subject = areastr+' Payment Confirmation'
                        lib.SendMail(sender=sender,proxy=proxy,to=to, \
                                     bcc=bcc,subject=subject,text=text)
                    changed.append({'etitle':etitle,'name':name,'free':free, \
                                    'email':email,'wec':wec,'pay':box,'delete':False})
                    break
        if delete:
            start = Get('start'+si)
            end = Get('end'+si)
            etitle = Get('etitle'+si)
            area = Get('area'+si)
            cs,url = lib.LoginCal(area)
            feed = lib.DateQuery(cs,url,start,end)
            for event in feed:
                if event['summary'] == etitle:
                    items = lib.RetrieveItems(event)
                    cost = items.get('wg_cost','?')
                    name = items.get('wg_name','?')
                    apt = items.get('wg_apt','?')
                    dfone = items.get('wg_dfone','?')
                    efone = items.get('wg_efone','?')
                    email = items.get('wg_email','?')
                    wec = items.get('wg_wec','?') == 'True'
                    free = items.get('wg_free','?') == 'True'
                    size = items.get('wg_size','?')
                    alc = items.get('wg_alc','?')
                    start = event['start']['dateTime']
                    end = event['end']['dateTime']
                    paystr = str(box)
                    content = {'name':name,'cost':cost,'apt':apt, \
                               'dfone':dfone,'efone':efone,'email':email, \
                               'wec':wec,'pay':paystr,'size':size, \
                               'alc':alc,'etitle':etitle,'start':start, \
                               'end':end,'free':free}
                    private,public = lib.CalContent(content)
                    lib.DeleteEvent(cs, url, event)
                    areastr = (lib.areas[0] == area)*'Lounge'+ \
                              (lib.areas[0] != area)*'Barbecue'+' Reservation'
                    text = \
"""
Your event has been deleted.
%(private)s""" % {'private':private}
                    sender = lib.emailsender
                    proxy = '"%(admin_name)s" <%(admin_email)s>' %{'admin_email':lib.admin_email,'admin_name':lib.admin_name}
                    to = '"%(name)s" <%(email)s>' % {'name':name,'email':email}
                    bcc = '"%(admin_name)s" <%(admin_email)s>' %{'admin_email':lib.admin_email,'admin_name':lib.admin_name}
                    subject = areastr+' Deletion Confirmation'
                    lib.SendMail(sender=sender,proxy=proxy,to=to, \
                        bcc=bcc,subject=subject,text=text)
                    changed.append({'etitle':etitle,'name':name,'free':False, \
                        'email':email,'wec':False,'pay':False,'delete':delete})
                    break
    if len(changed) == 0:
        status = 'No updates were made to payment status.'
    else:
        status = ''.join([StatusHtml(e) for e in changed])
    print 'Content-type: text/html'
    print
    print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Payment Update</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    <p class="left">
     Payment Update
     &#183; <a href="%(form)s">Reservation Application</a>
     &#183; <a href="%(main)s">Westgate Home</a>
    </p>
    <p class="right">
     <a href="%(admin)s">Admin</a>
    </p>
    <div class="clear"></div>
   </h3>
   <hr>
   <table>
    %(status)s
   </table>
  </div>
 </body>
</html>
""" % {'css':lib.css,'status':status,'main':lib.main,'form':lib.form, \
       'admin':lib.admin,'admin_email':lib.admin_email}
