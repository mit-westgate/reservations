import lib
import sys
from datetime import datetime
from datetime import timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    #log into the Lounge calendar
    cs,url = lib.LoginCal(lib.areas[0])
    #log into the BBQ calendar
    cs_bbq,url_bbq = lib.LoginCal(lib.areas[1])
    #find the 15minute interval to look at for cleaning emails
    now = datetime.now()
    cstart = now - timedelta(minutes = 15+(now.minute % 15), seconds = now.second, microseconds = now.microsecond )
    cstop = cstart + timedelta(minutes = 14, seconds = 59)
    #calculate the 15minute interval to look at for the reminder emails
    rstart=cstart+timedelta(days=1)
    rstop=cstop+timedelta(days=1)
    print cstart
    print cstop
    reminderEvents(cs,url,rstart,rstop)
    cleaningEvents(cs,url,cstart,cstop)
    reminderEvents_bbq(cs_bbq,url_bbq,rstart,rstop)
    cleaningEvents_bbq(cs_bbq,url_bbq,cstart,cstop)


def reminderEvents(cs,url,start,stop):
    strstart=start.strftime("%Y-%m-%dT%H:%M:%S.000")+lib.Tz2Str()
    strstop=stop.strftime("%Y-%m-%dT%H:%M:%S.000")+lib.Tz2Str()
    feed = lib.DateQuery(cs,url,strstart,strstop)
    events = feed
    #events = feed.entry
    if not events:
        return
    events.sort(cmp=lib.SortEvent)
    events=filter(lambda x:lib.KeepEvent(x,True,True),events)
    for e in events:
        try:
            einfo=getEvent(e)
            estart=lib.Goog2Dt(einfo['start'])
            estop=lib.Goog2Dt(einfo['end'])
            if (estart >= start) and (estart < stop):
                sendReminderEmail(einfo['name'],einfo['email'],einfo['etitle'],lib.Goog2Str(einfo['start']),lib.Goog2Str(einfo['end']))
        except:
            f=open('error_log.txt','a')
            f.write(einfo['name']+', '+einfo['email']+', '+einfo['etitle']+', '+start+', '+stop)
            f.write(sys.exc_info()[0])
            f.close()
            continue


def cleaningEvents(cs,url,start,stop):
    strstart=start.strftime("%Y-%m-%dT%H:%M:%S.000")+lib.Tz2Str()
    strstop=stop.strftime("%Y-%m-%dT%H:%M:%S.000")+lib.Tz2Str()
    feed = lib.DateQuery(cs,url,strstart,strstop)
    events = feed
    # events = feed.entry
    if not events:
        return
    events.sort(cmp=lib.SortEvent)
    events=filter(lambda x:lib.KeepEvent(x,True,True),events)
    for e in events:
        try:
            einfo=getEvent(e)
            estart=lib.Goog2Dt(einfo['start'])
            estop=lib.Goog2Dt(einfo['end'])
            if (estop >= (start+timedelta(minutes=15))) and (estop < (stop+timedelta(minutes=15))):
                print "sending the cleaning email"
                sendCleaningEmail(einfo['name'],einfo['email'],einfo['etitle'],lib.Goog2Str(einfo['start']),lib.Goog2Str(einfo['end']))
        except:
            f=open('error_log.txt','a')
            f.write(einfo['name']+', '+einfo['email']+', '+einfo['etitle']+', '+start+', '+stop)
            f.write(sys.exc_info()[0])
            f.close()
            continue


def reminderEvents_bbq(cs,url,start,stop):
    strstart=start.strftime("%Y-%m-%dT%H:%M:%S.000")+lib.Tz2Str()
    strstop=stop.strftime("%Y-%m-%dT%H:%M:%S.000")+lib.Tz2Str()
    feed = lib.DateQuery(cs,url,strstart,strstop)
    events = feed
    # events = feed.entry
    if not events:
        return
    events.sort(cmp=lib.SortEvent)
    events=filter(lambda x:lib.KeepEvent(x,True,True),events)
    for e in events:
        try:
            einfo=getEvent(e)
            estart=lib.Goog2Dt(einfo['start'])
            estop=lib.Goog2Dt(einfo['end'])
            if (estart >= start) and (estart < stop):
                sendReminderEmail_bbq(einfo['name'],einfo['email'],einfo['etitle'],lib.Goog2Str(einfo['start']),lib.Goog2Str(einfo['end']))
        except:
            f=open('error_log.txt','a')
            f.write(einfo['name']+', '+einfo['email']+', '+einfo['etitle']+', '+start+', '+stop)
            f.write(sys.exc_info()[0])
            f.close()
            continue


def cleaningEvents_bbq(cs,url,start,stop):
    strstart=start.strftime("%Y-%m-%dT%H:%M:%S.000")+lib.Tz2Str()
    strstop=stop.strftime("%Y-%m-%dT%H:%M:%S.000")+lib.Tz2Str()
    feed = lib.DateQuery(cs,url,strstart,strstop)
    events = feed
    # events = feed.entry
    if not events:
        return
    events.sort(cmp=lib.SortEvent)
    events=filter(lambda x:lib.KeepEvent(x,True,True),events)
    for e in events:
        try:
            einfo=getEvent(e)
            estart=lib.Goog2Dt(einfo['start'])
            estop=lib.Goog2Dt(einfo['end'])
            if (estop >= (start+timedelta(minutes=15))) and (estop < (stop+timedelta(minutes=15))):
                print "sending the cleaning email"
                sendCleaningEmail_bbq(einfo['name'],einfo['email'],einfo['etitle'],lib.Goog2Str(einfo['start']),lib.Goog2Str(einfo['end']))
        except:
            f=open('error_log.txt','a')
            f.write(einfo['name']+', '+einfo['email']+', '+einfo['etitle']+', '+start+', '+stop)
            f.write(sys.exc_info()[0])
            f.close()
            continue

def getEvent(event):
    items = lib.RetrieveItems(event)
    cost = items.get('wg_cost','0')
    name = items.get('wg_name','%(admin_name)s' % {'admin_name':lib.admin_name})
    apt = items.get('wg_apt',lib.admin_apt)
    dfone = items.get('wg_dfone','N/A')
    efone = items.get('wg_efone','N/A')
    email = items.get('wg_email','%(admin_email)s' % {'admin_email':lib.admin_email})
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
    # reg = event['published']
    reg = event['created']
    etitle = event['summary']
    startstr = lib.Goog2Str(start)
    endstr = lib.Goog2Str(end)
    regstr = lib.Goog2Str(reg)
    check = pay*' checked'
    return {'check':check,'cost':cost,'name':name,'etitle':etitle, \
       'startstr':startstr,'apt':apt,'dfone':dfone,'efone':efone, \
       'email':email,'endstr':endstr,'start':start,'end':end, \
       'regstr':regstr,'paystr':paystr,'clss':clss}


def sendReminderEmail(name,email,etitle,start_time,stop_time):
    sender = lib.emailsender
    proxy = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
    to = '"%(name)s" <%(email)s>' % {'name':name,'email':email}
    bcc = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
    subject = '%(area)s Reservation Reminder' % {'area':'Lounge'}

    text = \
"""
Event title: %(etitle)s
Event start:  %(start_time)s
Event end:  %(stop_time)s

This is a reminder email of your Lounge reservation tomorrow at the above times. We hope you have a great event! Please make sure to review the new lounge rules regarding cleaning of the lounge after your event (http://westgate.scripts.mit.edu/scripts/reservations/lounge.py). An email will be sent following your event end time with a cleaning checklist that you must fill out within 24 hours of the end of your event.
*****There is a $40 fee for not properly cleaning the lounge following your event*****""" % {'etitle':etitle,'start_time':start_time,'stop_time':stop_time}
    lib.SendMail(sender=sender,proxy=proxy,to=to,bcc=bcc,subject=subject,text=text)


def sendCleaningEmail(name,email,etitle,start_time,stop_time):
    sender = lib.emailsender
    proxy = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
    to = '"%(name)s" <%(email)s>' % {'name':name,'email':email}
    bcc = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
    subject = '%(area)s Reservation Confirmation' % {'area':'Lounge'}

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg['Bcc'] = bcc

    text = \
"""Please fill out the Westgate Lounge Cleaning checklist. This is REQUIRED:
https://docs.google.com/spreadsheet/viewform?formkey=dDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ"""

    html = \
    """<html style=""><body><div class="ss-email-body" style="width:576px;">If you have trouble viewing or submitting this form, you can fill it out online:
    <br>
    <a href="https://docs.google.com/spreadsheet/viewform?formkey=dDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ" style="">https://docs.google.com/spreadsheet/viewform?formkey=dDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ</a>
    <p></p>
    <div dir="ltr" style=""><div class="form-body" style=""><h1 class="ss-form-title" style="">Westgate Lounge Cleaning List</h1>
    <p></p></div>
    <div style="white-space: pre-wrap; display: inline">
    </div>
    <div class="form-body" style=""><div class="ss-form" style=""><form action="https://docs.google.com/spreadsheet/formResponse?formkey=dDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ&amp;ifq" method="POST" id="ss-form" style="">

    <br>
    <div class="errorbox-good" style="">
    <div class="ss-item ss-item-required ss-text" style=""><div class="ss-form-entry" style="margin-bottom:1.5em;zoom:1;"><label class="ss-q-title" for="entry_10" style="display:block;font-weight:bold;">Name:
    <span class="ss-required-asterisk" style="color:#c43b1d;">*</span></label>
    <label class="ss-q-help" for="entry_10" style="display:block;color:#666;margin:.1em 0 .25em 0;"></label>
    <input type="text" name="entry.10.single" value="" class="ss-q-short" id="entry_10" style=""></div></div></div>
    <br> <div class="errorbox-good" style="">
    <div class="ss-item  ss-checkbox" style=""><div class="ss-form-entry" style="margin-bottom:1.5em;zoom:1;"><label class="ss-q-title" for="entry_0" style="display:block;font-weight:bold;">Please check off each cleaning item below
    </label>
    <label class="ss-q-help" for="entry_0" style="display:block;color:#666;margin:.1em 0 .25em 0;"></label>
    <ul class="ss-choices" style="list-style:none;margin:.5em 0 0 0;padding:0;"><li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Wipe all tables and countertops with a clean, damp cloth" class="ss-q-checkbox" id="group_0_1" style="">
    Wipe all tables and countertops with a clean, damp cloth</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Wipe down the furniture with a slightly damp cloth." class="ss-q-checkbox" id="group_0_2" style="">
    Wipe down the furniture with a slightly damp cloth.</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Vacuum the carpeted area" class="ss-q-checkbox" id="group_0_3" style="">
    Vacuum the carpeted area</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Sweep the kitchen floor" class="ss-q-checkbox" id="group_0_4" style="">
    Sweep the kitchen floor</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Mop up all spills with a clean, damp mop after sweeping" class="ss-q-checkbox" id="group_0_5" style="">
    Mop up all spills with a clean, damp mop after sweeping</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Rinse out the sink" class="ss-q-checkbox" id="group_0_6" style="">
    Rinse out the sink</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Clean spills in the oven and on the stovetop" class="ss-q-checkbox" id="group_0_7" style="">
    Clean spills in the oven and on the stovetop</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Empty and clean the refrigerator and freezer" class="ss-q-checkbox" id="group_0_8" style="">
    Empty and clean the refrigerator and freezer</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Empty and replace all full garbage cans and recycling bins and replace with a new trash liner (found in trash rooms)" class="ss-q-checkbox" id="group_0_9" style="">
    Empty and replace all full garbage cans and recycling bins and replace with a new trash liner (found in trash rooms)</label></li> <li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.0.group" value="Place trashbags in a trash room or the Tang dumpsters" class="ss-q-checkbox" id="group_0_10" style="">
    Place trashbags in a trash room or the Tang dumpsters</label></li>
    </ul></div></div></div>
    <br> <div class="errorbox-good" style="">
    <div class="ss-item ss-item-required ss-checkbox" style=""><div class="ss-form-entry" style="margin-bottom:1.5em;zoom:1;"><label class="ss-q-title" for="entry_4" style="display:block;font-weight:bold;">Confirmation
    <span class="ss-required-asterisk" style="color:#c43b1d;">*</span></label>
    <label class="ss-q-help" for="entry_4" style="display:block;color:#666;margin:.1em 0 .25em 0;"></label>
    <ul class="ss-choices" style="list-style:none;margin:.5em 0 0 0;padding:0;"><li class="ss-choice-item" style="margin:0;line-height:1.3em;padding-bottom:.5em;"><label class="ss-choice-label" style=""><input type="checkbox" name="entry.4.group" value="By checking this box, I acknowledge I have cleaned the lounge, and agree to pay the $40 fine if the lounge is deemed unclean" class="ss-q-checkbox" id="group_4_1" style="">
    By checking this box, I acknowledge I have cleaned the lounge, and agree to pay the $40 fine if the lounge is deemed unclean</label></li>
    </ul></div></div></div>
    <br> <div class="errorbox-good" style="">
    <div class="ss-item  ss-paragraph-text" style=""><div class="ss-form-entry" style="margin-bottom:1.5em;zoom:1;"><label class="ss-q-title" for="entry_11" style="display:block;font-weight:bold;">General Comments (i.e lounge equipment problems, cleanliness of lounge before your event, ways to improve the lounge, etc.)
    </label>
    <label class="ss-q-help" for="entry_11" style="display:block;color:#666;margin:.1em 0 .25em 0;"></label>
    <textarea name="entry.11.single" rows="8" cols="75" class="ss-q-long" id="entry_11" style="max-width:90%;"></textarea></div></div></div>
    <br>
    <input type="hidden" name="pageNumber" value="0" style="">
    <input type="hidden" name="backupCache" style="">


    <div class="ss-item ss-navigate" style=""><div class="ss-form-entry" style="margin-bottom:1.5em;zoom:1;">
    <input type="submit" name="submit" value="Submit" style=""></div></div></form>
    </div>
    <div class="ss-footer" style=""><div class="ss-attribution" style=""></div>
    <div class="ss-legal" style=""><span class="ss-powered-by" style="color:#666;">Powered by <a href="http://docs.google.com" style="">Google Docs</a></span>
    <span class="ss-terms" style="display:block;clear:left;margin:1em 0.2em 0.2em;"><small><a href="https://docs.google.com/spreadsheet/reportabuse?formkey=dDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ&amp;source=https%253A%252F%252Fdocs.google.com%252Fspreadsheet%252Fviewform%253Fformkey%253DdDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ" style="">Report Abuse</a>
    -
    <a href="http://www.google.com/accounts/TOS" style="">Terms of Service</a>
    -
    <a href="http://www.google.com/google-d-s/terms.html" style="">Additional Terms</a></small></span></div></div></div></div>
    <br>
    <style type="text/css" media="screen" style="">
              .form-body{display:none;}
            </style></div></body></html>"""

    part1 = MIMEText(text, 'plain','latin_1')
    part2 = MIMEText(html, 'html','latin_1')

    msg.attach(part1)
    msg.attach(part2)

    recipients = (',').join([to,bcc]).split(',')

    s = smtplib.SMTP('outgoing.mit.edu')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()


def sendReminderEmail_bbq(name,email,etitle,start_time,stop_time):
    sender = lib.emailsender
    proxy = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
    to = '"%(name)s" <%(email)s>' % {'name':name,'email':email}
    bcc = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
    subject = '%(area)s Reservation Reminder' % {'area':'BBQ'}

    text = \
"""
Event title: %(etitle)s
Event start:  %(start_time)s
Event end:  %(stop_time)s

This is a reminder email of your BBQ reservation tomorrow at the above times. We hope you have a great event! Please plan on cleaning up afterwards so others can enjoy the space after your event. Remember to bring trash bags outside to collect  trash from your event. You can find them in the trash rooms (where you usually bring your everyday trash). An email will be sent following your event end time with a cleaning instructions. 
*****There is a $40 fee for not properly cleaning the BBQ area following your event*****""" % {'etitle':etitle,'start_time':start_time,'stop_time':stop_time}
    lib.SendMail(sender=sender,proxy=proxy,to=to,bcc=bcc,subject=subject,text=text)


def sendCleaningEmail_bbq(name,email,etitle,start_time,stop_time):
    sender = lib.emailsender
    proxy = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
    to = '"%(name)s" <%(email)s>' % {'name':name,'email':email}
    bcc = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
    subject = '%(area)s Reservation Reminder' % {'area':'BBQ'}

    text = \
"""
Event title: %(etitle)s
Event start:  %(start_time)s
Event end:  %(stop_time)s

This is a reminder email to clean up the BBQ area after your event. Please make sure there is no trash left on or underneath the picnic area as well. Bring any trash bags inside your building and place them in the trash rooms. Do not leave trash bags outdoors. Also, do a quick walkthrough of the courtyard and playground area to ensure there is no trash from your event. Items like wrappers and popped balloons can easily make their way out of the picnic area, especially when there are children involved. 
*****There is a $40 fee for not properly cleaning the BBQ area following your event*****""" % {'etitle':etitle,'start_time':start_time,'stop_time':stop_time}
    lib.SendMail(sender=sender,proxy=proxy,to=to,bcc=bcc,subject=subject,text=text)

#run the main program
if __name__ == "__main__":
    main()
