import random
import hashlib
import collections
import functools
import subprocess
import json
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for
from flask import g
from flask import make_response
from flask import send_from_directory
import os
from email.mime.text import MIMEText

from datetime import datetime

from Reservation import Reservation
from GoogleCalendar import GoogleCalendar
from Helper import send_mail, check_admin

Reservation.init_database()
calendar = GoogleCalendar()

app = Flask(__name__, template_folder='./templates', static_url_path='/static')
app.debug = True


@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

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
    is_wec = False if request.form.get("is_wec_event") is None else True
    is_hundred_or_more = True if int(request.form.get("hundred")) == 1 else False
    alcohol_type = int(request.form.get("alcohol"))

    start_time = Reservation.form_to_datetime(date, starts)
    end_time = Reservation.form_to_datetime(date, ends)

    reservation = Reservation(
            first_name,
            last_name,
            email,
            apartment,
            place_id,
            event_name,
            admit,
            start_time,
            end_time,
            is_wec,
            is_hundred_or_more,
            alcohol_type
            );

    # received data will be serialized into json

    return render_template("confirm.html",
            r=reservation.get_obj(),
            json_data = reservation.to_json()
            )

@app.route('/check', methods=['POST'])
def check():
    json_data = json.loads(request.form.get("json_data"))
    r = Reservation.from_json(json_data)
    start_time = r.render_time()

    err = r.check(calendar)
    
    if (err is None) :

        r.add(calendar)

        return render_template("success.html",
            place = json_data['place'],
            event_name=r.event_name,
            start_time=start_time
        )
    else :
        return render_template("error.html",
            err=err 
        )
    
@app.after_request
def disable_xss_protection(response):
    response.headers.add('X-XSS-PROTECTION', '0')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

