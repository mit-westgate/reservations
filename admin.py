#!/usr/bin/python
from datetime import datetime
import sys
import cgi
import json
from jinja2 import Environment, PackageLoader, select_autoescape

from Helper import check_admin
from Reservation import Reservation
from GoogleCalendar import GoogleCalendar

env = Environment(
        loader = PackageLoader('reservations', 'templates'),
        autoescape = select_autoescape(['html', 'xml'])
)

url = "https://yasushis.scripts.mit.edu:444/reservations/admin"

print "Content-type: text/html\n\n"

if not check_admin() :
    template = env.get_template("error.html")
    print template.render(err="either you don't have a MIT certificate or not a super user. You can try visit this {url}".format(url=url))
    sys.exit()

form = cgi.FieldStorage()
now = datetime.now()
try:
    month = int(form.get("month"))
except:
    month = now.month

try :
    year = int(form.get("year"))
except:
    year = now.year

del_count = 0
update_pay_count = 0
deletes = form.getlist("delete")
update_pay = form.getlist("update_pay")

if len(deletes) > 0:
    calendar = GoogleCalendar()

for r_id in form.getlist("ids"):
    r = Reservation.select_by_event_id(r_id)
    if r_id in deletes:
        r.delete(calendar)
        del_count += 1
        continue
    if not r.did_pay is (r_id in update_pay):
        r.update_did_pay(not r.did_pay)
        update_pay_count += 1

result = Reservation.select_two_months(year, month)

if (del_count + update_pay_count) > 0:
    status_line = "deleted: {}, updated pay status: {}".format(del_count, update_pay_count)
else:
    status_line = ""
        
template = env.get_template("admin.html")
print template.render(month=month,year=year, reservations = result, status_line = status_line)
