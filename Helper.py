# helper functions

import smtplib
import os

from config import super_users

def send_mail(sender = '',proxy = None,to='',cc='',bcc='',subject='',text=''):
    if proxy == None:
        proxy = sender
    message = 'From: {}\nTo: {}\nCc: {}\nBcc: {}\nSubject: {}\n\n{}'.format(proxy,to,cc,bcc,subject,text)
    recipients = (',').join([to,cc,bcc]).split(',')
    server = smtplib.SMTP('outgoing.mit.edu')

    try:
        server.sendmail(sender, recipients, message)
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

def check_admin():
    # are we accessing through port 444?

    try:
        mit_email= os.environ["SSL_CLIENT_S_DN_Email"]
    except:
        return False

    user_name = mit_email.split("@")[0]

    # is the user a super user?
    return user_name in super_users

    


