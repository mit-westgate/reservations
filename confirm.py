#!/usr/bin/python

import cgitb;cgitb.enable()
import lib,cgi

if not lib.IsSecure():
    lib.SecureRedirect()
else:
    form = cgi.FieldStorage()
    p = lib.ProcessForm(form,ispay=True)
    if len(p['errors']) > 0:
        errors = '<ul>\n<li>'+'</li>\n<li>'.join(p['errors'])+'</li>\n</ul>'
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
    User Error
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
   </h3>
   <hr>
   Your form submission generated the following errors and warnings.
   Please go back and try again.
   %(errors)s
  </div>
 </body>
</html>
""" % {'css':lib.css,'errors':errors,'form':lib.form,'main':lib.main}
    else:
        name = '%(ntitle)s %(gname)s %(fname)s' % p
        pay = 'False'
        content = {'name':name,'cost':p['cost'],'apt':p['apt'],'dfone':p['dfone'], \
                   'efone':p['efone'],'email':p['email'],'wec':p['wec'],'pay':pay, \
                   'size':p['size'],'alc':p['alc'],'etitle':p['etitle'], \
                   'start':p['start'],'end':p['end'],'free':p['free']}
        items = {'wg_name':name,'wg_cost':p['cost'],'wg_apt':p['apt'], \
                 'wg_dfone':p['dfone'],'wg_efone':p['efone'], \
                 'wg_email':p['email'],'wg_wec':str(p['wec']),'wg_pay':pay, \
                 'wg_size':p['size'],'wg_alc':p['alc'],'wg_free':str(p['free'])}
        private,public = lib.CalContent(content)
        event = lib.InsertEvent(p['cs'],p['url'],p['etitle'],public,p['area'], \
                                p['start'],p['end'],items)
        paydir = (not p['wec'] and not p['free'])*( \
"""Please deposit $%(cost)s in the %(money_collect_name)s drop box outside of
apartment %(money_collect_room)s. Please use checks only, made payable to MIT. Place the
check inside of an envelope labeled with your name, the reservation location,
and the date and time of the event. Once your check has been processed by the
%(money_collect_name)ss you will receive another confirmation e-mail.
""" % {'cost':p['cost'],'money_collect_room':lib.money_collect_room,'money_collect_name':lib.money_collect_name}).replace('\n',' ').replace('\r','')
        sender = lib.emailsender
        proxy = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
        to = '"%(name)s" <%(email)s>' % {'name':name,'email':p['email']}
        bcc = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
        subject = '%(area)s Reservation Confirmation' % {'area':p['area']}
        text = \
"""The event "%(etitle)s" has been successfully registered. %(paydir)s
%(private)s""" % {'etitle':p['etitle'],'paydir':paydir,'private':private}
        lib.SendMail(sender=sender,proxy=proxy,to=to,bcc=bcc,subject=subject,text=text)
        if p['free'] and not p['wec']:
            freedb = lib.File2Param(lib.freedb,'d')
            uid = lib.GetAttributes('uid')
            office = lib.Uid2Office(uid)
            freedb[office] = max(freedb[office]-p['cost']/lib.costperblk,0)
            lib.Param2File(freedb,lib.freedb)    
        print 'Content-type: text/html'
        print
        print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Registration Successful</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    Registration Successful
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
   </h3>
   <hr>
   The event <strong>%(etitle)s</strong> has been sucessfully registered. A
   confirmation e-mail has been sent to %(name)s at
   <a href="mailto:%(email)s">%(email)s</a>. %(paydir)s
  </div>
 </body>
</html>
""" % {'css':lib.css,'etitle':p['etitle'],'name':name, \
       'email':p['email'],'paydir':paydir,'form':lib.form,'main':lib.main}
