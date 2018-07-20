import lib

#Required inputs: name,email,start_time, stop_time
name='Michael Churchill'
email='rmchurch@mit.edu'

sender = lib.emailsender
proxy = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
to = '"%(name)s" <%(email)s>' % {'name':name,'email':email}#p['email']}
bcc = '"%(admin_name)s" <%(admin_email)s>' % {'admin_email':lib.admin_email,'admin_name':lib.admin_name}
subject = '%(area)s Reservation Confirmation' % {'area':'Lounge'}#p['area']}

text = \
"""This is a reminder email of your Lounge reservation tommorrow, from start_time to stop_time. We hope you have a great event! Please make sure to review the new lounge rules (http://westgate.mit.edu/scripts/reservations/lounge.py) regarding cleaning of the lounge after your event. An email will be sent following your event end time with a cleaning checklist that you must fill out within 24 hours of your event.
*****There is a $30 fee for not properly cleaning the lounge following your event*****"""
lib.SendMail(sender=sender,proxy=proxy,to=to,bcc=bcc,subject=subject,text=text)
