import random
import hashlib
import collections
import functools
import subprocess
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for
from flask import g
from flask import make_response
from email.mime.text import MIMEText

from Reservation import Reservation

import sqlite3
conn = sqlite3.connect('reservations_db.sqlite')

cursor = conn.cursor()
Reservation.setup_database(cursor)

# r = Reservation("Yasushi", "Sakai", "ysshski@gmail.com","706", 0, "birthday", "hjkloi", 89008, 1588304, 0, 1, 0 )
# r.add_record(cursor);

print Reservation.select_all(cursor)

app = Flask(__name__, template_folder='./templates', static_url_path='/static')
app.debug = True

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/confirm', methods=['POST'])
def confirm():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get('email')
    apartment = request.form.get("apartment")
    place_id = int(request.form.get("place"))
    event_name = request.form.get("event_name")
    admit = request.form.get("admit_one")
    date = request.form.get("date")
    starts = request.form.get("starts")
    ends = request.form.get("ends")
    is_wec = request.form.get("is_wec_event")
    is_hundred_or_more = int(request.form.get("hundred"))
    alcohol_type = int(request.form.get("alcohol"))

    name = "{} {}".format(first_name, last_name)
    place = "Lounge" if place_id is 0 else "BBQ"
    hundred = "no" if is_hundred_or_more is 0 else "yes"
    
    if (alcohol_type is 0):
        alcohol = "not serving alcohol"
    elif (alcohol_type is 1):
        alcohol = "serving, guests less than 50"
    else:
        alcohol = "serving, guest more than 50"



    reservation = Reservation(
            first_name,
            last_name,
            email,
            apartment,
            place_id,
            event_name,
            admit,
            date,
            starts,
            ends,
            is_wec,
            is_hundred_or_more,
            alcohol_type
            );

    # TODO: SUPER REDUNDANT!!!
    
    return render_template("confirm.html",
            r=reservation.get_obj(),
            json_data = reservation.to_json()
            )

@app.route('/success', methods=['POST'])
def success():
    print request.form.get("json_data")
    return render_template("success.html")

# app.add_url_rule('/success', 'success', success, methods=['GET'])
# app.add_url_rule('/admin', 'admin', admin, methods=['GET'])

@app.after_request
def disable_xss_protection(response):
    response.headers.add('X-XSS-PROTECTION', '0')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

