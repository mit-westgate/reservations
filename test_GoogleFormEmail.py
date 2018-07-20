import lib
import smtplib
import quopri
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.encoders as e
#Required inputs: name,email,start_time, stop_time
name='Michael Churchill'
email='rmchurch@mit.edu'

sender = lib.emailsender
proxy = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
to = '"%(name)s" <%(email)s>' % {'name':name,'email':email}
bcc = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
subject = '%(area)s Reservation Confirmation' % {'area':'Lounge'}

msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = email

#text = \
#"""If you have trouble viewing or submitting this form, you can fill it out
#online:
#https://docs.google.com/spreadsheet/viewform?formkey=dDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ
#
#
#Westgate Lounge Cleaning List
#
#
#Name: *
#
#
#
#Please check off each cleaning item below
#
#Wipe all tables and countertops with a clean, damp cloth
#Wipe down the furniture with a slightly damp cloth.
#Vacuum the carpeted area
#Sweep the kitchen floor
#Mop up all spills with a clean, damp mop after sweeping
#Rinse out the sink
#Clean spills in the oven and on the stovetop
#Empty and clean the refrigerator and freezer
#Empty and replace all full garbage cans and recycling bins and replace with
#a new trash liner (found in trash rooms)
#Place trashbags in a trash room or the Tang dumpsters
#
#
#Confirmation *
#
#By checking this box, I acknowledge I have cleaned the lounge, and agree to
#pay the $40 fine if the lounge is deemed unclean
#
#
#General Comments (ie lounge equipment problems, cleanliness of lounge
#before your event, ways to improve the lounge, etc.)
#
#
#
#Powered by Google Docs Report Abuse - Terms of Service - Additional Terms"""

text = \
"""If you have trouble viewing or submitting this form, you can fill it out
online:
https://docs.google.com/spreadsheet/viewform?formkey=dDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ


Westgate Lounge Cleaning List


Name: *



Please check off each cleaning item below

Wipe all tables and countertops with a clean, damp cloth
Wipe down the furniture with a slightly damp cloth.
Vacuum the carpeted area
Sweep the kitchen floor
Mop up all spills with a clean, damp mop after sweeping
Rinse out the sink
Clean spills in the oven and on the stovetop
Empty and clean the refrigerator and freezer
Empty and replace all full garbage cans and recycling bins and replace with
a new trash liner (found in trash rooms)
Place trashbags in a trash room or the Tang dumpsters


Confirmation *

By checking this box, I acknowledge I have cleaned the lounge, and agree to
pay the $40 fine if the lounge is deemed unclean


General Comments (ie lounge equipment problems, cleanliness of lounge
before your event, ways to improve the lounge, etc.)



Powered by Google Docs Report Abuse - Terms of Service - Additional Terms"""


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


#html = \
#"""<html style=3D""><body><div class=3D"ss-email-body" style=3D"width:576px;">=
#If you have trouble viewing or submitting this form, you can fill it out on=
#line:
#<br>
#<a href=3D"https://docs.google.com/spreadsheet/viewform?formkey=3DdDhwMTFNS=
#WVQeURxYy1KMDZCRlJ3aFE6MQ" style=3D"">https://docs.google.com/spreadsheet/v=
#iewform?formkey=3DdDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ</a>
#<p></p>
#<div dir=3D"ltr" style=3D""><div class=3D"form-body" style=3D""><h1 class=
#=3D"ss-form-title" style=3D"">Westgate Lounge Cleaning List</h1>
#<p></p></div>
#<div style=3D"white-space: pre-wrap; display: inline">
#</div>
#<div class=3D"form-body" style=3D""><div class=3D"ss-form" style=3D""><form=
# action=3D"https://docs.google.com/spreadsheet/formResponse?formkey=3DdDhwM=
#TFNSWVQeURxYy1KMDZCRlJ3aFE6MQ&amp;ifq" method=3D"POST" id=3D"ss-form" style=
#=3D"">
#
#<br>
#<div class=3D"errorbox-good" style=3D"">
#<div class=3D"ss-item ss-item-required ss-text" style=3D""><div class=3D"ss=
#-form-entry" style=3D"margin-bottom:1.5em;zoom:1;"><label class=3D"ss-q-tit=
#le" for=3D"entry_10" style=3D"display:block;font-weight:bold;">Name:
#<span class=3D"ss-required-asterisk" style=3D"color:#c43b1d;">*</span></lab=
#el>
#<label class=3D"ss-q-help" for=3D"entry_10" style=3D"display:block;color:#6=
#66;margin:.1em 0 .25em 0;"></label>
#<input type=3D"text" name=3D"entry.10.single" value=3D"" class=3D"ss-q-shor=
#t" id=3D"entry_10" style=3D""></div></div></div>
#<br> <div class=3D"errorbox-good" style=3D"">
#<div class=3D"ss-item  ss-checkbox" style=3D""><div class=3D"ss-form-entry"=
# style=3D"margin-bottom:1.5em;zoom:1;"><label class=3D"ss-q-title" for=3D"e=
#ntry_0" style=3D"display:block;font-weight:bold;">Please check off each cle=
#aning item below
#</label>
#<label class=3D"ss-q-help" for=3D"entry_0" style=3D"display:block;color:#66=
#6;margin:.1em 0 .25em 0;"></label>
#<ul class=3D"ss-choices" style=3D"list-style:none;margin:.5em 0 0 0;padding=
#:0;"><li class=3D"ss-choice-item" style=3D"margin:0;line-height:1.3em;paddi=
#ng-bottom:.5em;"><label class=3D"ss-choice-label" style=3D""><input type=3D=
#"checkbox" name=3D"entry.0.group" value=3D"Wipe all tables and countertops =
#with a clean, damp cloth" class=3D"ss-q-checkbox" id=3D"group_0_1" style=3D=
#"">
#Wipe all tables and countertops with a clean, damp cloth</label></li> <li c=
#lass=3D"ss-choice-item" style=3D"margin:0;line-height:1.3em;padding-bottom:=
#.5em;"><label class=3D"ss-choice-label" style=3D""><input type=3D"checkbox"=
# name=3D"entry.0.group" value=3D"Wipe down the furniture with a slightly da=
#mp cloth." class=3D"ss-q-checkbox" id=3D"group_0_2" style=3D"">
#Wipe down the furniture with a slightly damp cloth.</label></li> <li class=
#=3D"ss-choice-item" style=3D"margin:0;line-height:1.3em;padding-bottom:.5em=
#;"><label class=3D"ss-choice-label" style=3D""><input type=3D"checkbox" nam=
#e=3D"entry.0.group" value=3D"Vacuum the carpeted area" class=3D"ss-q-checkb=
#ox" id=3D"group_0_3" style=3D"">
#Vacuum the carpeted area</label></li> <li class=3D"ss-choice-item" style=3D=
#"margin:0;line-height:1.3em;padding-bottom:.5em;"><label class=3D"ss-choice=
#-label" style=3D""><input type=3D"checkbox" name=3D"entry.0.group" value=3D=
#"Sweep the kitchen floor" class=3D"ss-q-checkbox" id=3D"group_0_4" style=3D=
#"">
#Sweep the kitchen floor</label></li> <li class=3D"ss-choice-item" style=3D"=
#margin:0;line-height:1.3em;padding-bottom:.5em;"><label class=3D"ss-choice-=
#label" style=3D""><input type=3D"checkbox" name=3D"entry.0.group" value=3D"=
#Mop up all spills with a clean, damp mop after sweeping" class=3D"ss-q-chec=
#kbox" id=3D"group_0_5" style=3D"">
#Mop up all spills with a clean, damp mop after sweeping</label></li> <li cl=
#ass=3D"ss-choice-item" style=3D"margin:0;line-height:1.3em;padding-bottom:.=
#5em;"><label class=3D"ss-choice-label" style=3D""><input type=3D"checkbox" =
#name=3D"entry.0.group" value=3D"Rinse out the sink" class=3D"ss-q-checkbox"=
# id=3D"group_0_6" style=3D"">
#Rinse out the sink</label></li> <li class=3D"ss-choice-item" style=3D"margi=
#n:0;line-height:1.3em;padding-bottom:.5em;"><label class=3D"ss-choice-label=
#" style=3D""><input type=3D"checkbox" name=3D"entry.0.group" value=3D"Clean=
# spills in the oven and on the stovetop" class=3D"ss-q-checkbox" id=3D"grou=
#p_0_7" style=3D"">
#Clean spills in the oven and on the stovetop</label></li> <li class=3D"ss-c=
#hoice-item" style=3D"margin:0;line-height:1.3em;padding-bottom:.5em;"><labe=
#l class=3D"ss-choice-label" style=3D""><input type=3D"checkbox" name=3D"ent=
#ry.0.group" value=3D"Empty and clean the refrigerator and freezer" class=3D=
#"ss-q-checkbox" id=3D"group_0_8" style=3D"">
#Empty and clean the refrigerator and freezer</label></li> <li class=3D"ss-c=
#hoice-item" style=3D"margin:0;line-height:1.3em;padding-bottom:.5em;"><labe=
#l class=3D"ss-choice-label" style=3D""><input type=3D"checkbox" name=3D"ent=
#ry.0.group" value=3D"Empty and replace all full garbage cans and recycling =
#bins and replace with a new trash liner (found in trash rooms)" class=3D"ss=
#-q-checkbox" id=3D"group_0_9" style=3D"">
#Empty and replace all full garbage cans and recycling bins and replace with=
# a new trash liner (found in trash rooms)</label></li> <li class=3D"ss-choi=
#ce-item" style=3D"margin:0;line-height:1.3em;padding-bottom:.5em;"><label c=
#lass=3D"ss-choice-label" style=3D""><input type=3D"checkbox" name=3D"entry.=
#0.group" value=3D"Place trashbags in a trash room or the Tang dumpsters" cl=
#ass=3D"ss-q-checkbox" id=3D"group_0_10" style=3D"">
#Place trashbags in a trash room or the Tang dumpsters</label></li>
#</ul></div></div></div>
#<br> <div class=3D"errorbox-good" style=3D"">
#<div class=3D"ss-item ss-item-required ss-checkbox" style=3D""><div class=
#=3D"ss-form-entry" style=3D"margin-bottom:1.5em;zoom:1;"><label class=3D"ss=
#-q-title" for=3D"entry_4" style=3D"display:block;font-weight:bold;">Confirm=
#ation
#<span class=3D"ss-required-asterisk" style=3D"color:#c43b1d;">*</span></lab=
#el>
#<label class=3D"ss-q-help" for=3D"entry_4" style=3D"display:block;color:#66=
#6;margin:.1em 0 .25em 0;"></label>
#<ul class=3D"ss-choices" style=3D"list-style:none;margin:.5em 0 0 0;padding=
#:0;"><li class=3D"ss-choice-item" style=3D"margin:0;line-height:1.3em;paddi=
#ng-bottom:.5em;"><label class=3D"ss-choice-label" style=3D""><input type=3D=
#"checkbox" name=3D"entry.4.group" value=3D"By checking this box, I acknowle=
#dge I have cleaned the lounge, and agree to pay the $40 fine if the lounge =
#is deemed unclean" class=3D"ss-q-checkbox" id=3D"group_4_1" style=3D"">
#By checking this box, I acknowledge I have cleaned the lounge, and agree to=
# pay the $40 fine if the lounge is deemed unclean</label></li>
#</ul></div></div></div>
#<br> <div class=3D"errorbox-good" style=3D"">
#<div class=3D"ss-item  ss-paragraph-text" style=3D""><div class=3D"ss-form-=
#entry" style=3D"margin-bottom:1.5em;zoom:1;"><label class=3D"ss-q-title" fo=
#r=3D"entry_11" style=3D"display:block;font-weight:bold;">General Comments (=
#i.e lounge equipment problems, cleanliness of lounge before your event, way=
#s to improve the lounge, etc.)
#</label>
#<label class=3D"ss-q-help" for=3D"entry_11" style=3D"display:block;color:#6=
#66;margin:.1em 0 .25em 0;"></label>
#<textarea name=3D"entry.11.single" rows=3D"8" cols=3D"75" class=3D"ss-q-lon=
#g" id=3D"entry_11" style=3D"max-width:90%;"></textarea></div></div></div>
#<br>
#<input type=3D"hidden" name=3D"pageNumber" value=3D"0" style=3D"">
#<input type=3D"hidden" name=3D"backupCache" style=3D"">
#
#
#<div class=3D"ss-item ss-navigate" style=3D""><div class=3D"ss-form-entry" =
#style=3D"margin-bottom:1.5em;zoom:1;">
#<input type=3D"submit" name=3D"submit" value=3D"Submit" style=3D""></div></=
#div></form>
#</div>
#<div class=3D"ss-footer" style=3D""><div class=3D"ss-attribution" style=3D"=
#"></div>
#<div class=3D"ss-legal" style=3D""><span class=3D"ss-powered-by" style=3D"c=
#olor:#666;">Powered by <a href=3D"http://docs.google.com" style=3D"">Google=
# Docs</a></span>
#<span class=3D"ss-terms" style=3D"display:block;clear:left;margin:1em 0.2em=
# 0.2em;"><small><a href=3D"https://docs.google.com/spreadsheet/reportabuse?=
#formkey=3DdDhwMTFNSWVQeURxYy1KMDZCRlJ3aFE6MQ&amp;source=3Dhttps%253A%252F%2=
#52Fdocs.google.com%252Fspreadsheet%252Fviewform%253Fformkey%253DdDhwMTFNSWV=
#QeURxYy1KMDZCRlJ3aFE6MQ" style=3D"">Report Abuse</a>
#-
#<a href=3D"http://www.google.com/accounts/TOS" style=3D"">Terms of Service<=
#/a>
#-
#<a href=3D"http://www.google.com/google-d-s/terms.html" style=3D"">Addition=
#al Terms</a></small></span></div></div></div></div>
#<br>
#<style type=3D"text/css" media=3D"screen" style=3D"">
#          .form-body{display:none;}
#        </style></div></body></html>"""

#html=quopri.decodestring(html)

part1 = MIMEText(text, 'plain','latin_1')
#part1.set_charset('latin_1')
part2 = MIMEText(html, 'html','latin_1')
#part2.set_charset('latin_1')
#f=open('decoded.txt','w')
#f.write(text)
#f.write('\n')
#f.write(html)

#this just ends up putting two Content-Transfer-Encoding: quoted-printable headers, and messes
#up the quoted printable
#e.encode_quopri(part1)
#e.encode_quopri(part2)

msg.attach(part1)
msg.attach(part2)

s = smtplib.SMTP('outgoing.mit.edu')
s.sendmail(sender, email, msg.as_string())
s.quit()
#lib.SendMail(sender=sender,proxy=proxy,to=to,bcc=bcc,subject=subject,text=text)