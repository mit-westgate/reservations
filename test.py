#!/usr/bin/python

import pprint
import sys
import cgi
from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

"""
# web service version

web_client_id='117593083049-2s35vfflg35u5f45s9aqv1hj4vmcs9ap.apps.googleusercontent.com'
web_client_secret='QzlP8bOIrk8KyvmKwWuujVE5'

flow = OAuth2WebServerFlow(client_id=web_client_id,
                           client_secret=web_client_secret,
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='http://westgate.scripts.mit.edu/scripts/reservations/test.py')
form = cgi.FieldStorage()
if(not(form.has_key('code'))):
    # code = '4/6k0Ch-7DxEl2cyCDSHU87tBFTc6EIipdkDXoZ81kxII.YtwKbEGCVmMaJvIeHux6iLYPkJmTkwI'
    auth_uri = flow.step1_get_authorize_url()

    print "Content-Type: text/plain"
    print "Refresh: 0; url=%s" % auth_uri
    print
    print "Redirecting..."
    sys.exit()

code = form['code'].value

print "Content-Type: text/plain"
print
print "Passed back"

print code
credentials = flow.step2_exchange(code)    
print "calling creds"

"""

# service version

client_email = '117593083049-h1pupclppqu21eepcskepfabsu2ghh15@developer.gserviceaccount.com'
private_key_file = 'ReservationSystem.p12'
with open(private_key_file) as f:
  private_key = f.read()
credentials = SignedJwtAssertionCredentials(client_email, private_key,
    'https://www.googleapis.com/auth/calendar')

http_auth = credentials.authorize(Http())
print "done calling creds"

"""
# API key only used in non oAuth settings whiceh are not allowed for calendar access

api_key = 'AIzaSyA2da8OCLfy2IiANv2hR-YbSPdhM6z8bdE'
print api_key
"""

service = build('calendar', 'v3',http=http_auth)
pprint.pprint(service)
print service
print "built service"
request = service.calendarList().list()
pprint.pprint(request)
print request
print "built request"
response = request.execute()
print "got response back"
pprint.pprint(response)
print "This should be empty for service version"

lounge_id = 'jbt1onapg3ffroh27umi9qm4ic@group.calendar.google.com'
bbq_id = 'tjsllo1pojk4tpcp40l8pinseg@group.calendar.google.com'

request = service.events().list(calendarId=lounge_id)
print request.execute()




