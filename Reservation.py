from datetime import datetime
from calendar import monthrange
from time import mktime
import pytz
import json

from Helper import send_mail
from config import admin_email, database_file

import sqlite3

eastern_time = pytz.timezone('America/New_York')

class Reservation:

    @staticmethod
    def init_database():

        with sqlite3.connect(database_file) as con:
            cursor = con.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS reservations ( \
                id INTEGER PRIMARY KEY, \
                event_id TEXT, \
                first_name TEXT, \
                last_name TEXT, \
                email TEXT, \
                apartment TEXT, \
                place_id INTEGER, \
                event_name TEXT, \
                adMitOne TEXT, \
                start_time TEXT, \
                end_time TEXT,\
                is_wec INTEGER, \
                is_hundred_or_more INTEGER, \
                alcohol_type INTEGER, \
                did_pay INTEGER);")

            con.commit()

    @staticmethod
    def select_all():
        with sqlite3.connect(database_file) as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM reservations")
            return [Reservation.from_record(r) for r in cursor.fetchall()]

    @staticmethod
    def select_month(year, month):
        with sqlite3.connect(database_file) as con:
            cursor = con.cursor()
            _, last_day = monthrange(year, month)
            month = '{0:02d}'.format(month)
            q = "SELECT * FROM reservations WHERE start_time BETWEEN '{year}-{month}-01' AND '{year}-{month}-{last_day}'".format(
                year = year,
                month = month,
                last_day = last_day
                )
            cursor.execute(q)
            return [Reservation.from_record(r) for r in cursor.fetchall()]

    @staticmethod
    def select_by_event_id(eid):
        with sqlite3.connect(database_file) as con:
            cursor = con.cursor()
            q = "SELECT * FROM reservations WHERE event_id='{}'".format(eid)
            cursor.execute(q)
            return Reservation.from_record(cursor.fetchone())

    @staticmethod
    def form_to_datetime(date, time):
        str_time = "{} {}".format(date, time)
        return eastern_time.localize(datetime.strptime(str_time, "%Y-%m-%d %H:%M"))

    def check(self, calendar):
        # def list_events(self, calendar_id, time_min, time_max):

        result = calendar.list_events(self.get_place(), self.start_time, self.end_time)

        if len(result) == 0 :
            return None
        else :
            return "conflicting event found"

        return None

    @staticmethod
    def parse_datetime(str_date_time):
        return eastern_time.localize(datetime.strptime(str_date_time, "%Y-%m-%d %H:%M:%S.%f"))

    @staticmethod
    def from_json(j):

        start_time = Reservation.parse_datetime(j["start_time"])
        end_time = Reservation.parse_datetime(j["end_time"])

        return Reservation(
                j['first_name'],
                j['last_name'],
                j['email'],
                j['apartment'],
                j['place_id'],
                j['event_name'],
                j['adMitOne'],
                start_time,
                end_time,
                j['is_wec'],
                j['is_hundred_or_more'],
                j['alcohol_type']
                )

    @staticmethod
    def from_record(record):
        record = list(record)
        record[9] = Reservation.parse_datetime(record[9])
        record[10] = Reservation.parse_datetime(record[10])
        r = Reservation(*record[2:14])
        r.id = record[0]
        r.event_id = record[1]
        r.is_wec = True if record[11] is 1 else False
        r.is_hundred_or_more = True if record[12] is 1 else False
        r.did_pay = True if record[14] is 1 else False

        return r
        
    def __init__(self, first_name, last_name, email, apartment, place_id, event_name, adMitOne, start_time, end_time, is_wec, is_hundred_or_more, alcohol_type):
        
        self.id = -1
        self.event_id = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.apartment = apartment
        self.place_id = place_id
        self.event_name = event_name
        self.adMitOne = adMitOne
        self.start_time = start_time        
        self.end_time = end_time
        self.is_wec = is_wec
        self.is_hundred_or_more = is_hundred_or_more
        self.alcohol_type = alcohol_type
        self.did_pay = is_wec or not adMitOne == ""

    def add_record(self):

        with sqlite3.connect(database_file) as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO reservations (event_id, first_name, last_name, email, apartment, place_id, event_name, adMitOne, start_time, end_time, is_wec, is_hundred_or_more, alcohol_type, did_pay) VALUES ('{ei}','{fn}', '{ln}', '{em}', '{ap}', {pl}, '{en}', '{ad}', '{st}', '{et}', {iw}, {ih}, {at}, {dp})".format(
            ei = self.event_id,
            fn = self.first_name,
            ln = self.last_name,
            em = self.email,
            ap = self.apartment,
            pl = self.place_id,
            en = self.event_name,
            ad = self.adMitOne,
            st = self.start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            et = self.end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            iw = 1 if self.is_wec else 0,
            ih = 1 if self.is_hundred_or_more else 0, 
            at = self.alcohol_type,
            dp = 1 if self.did_pay else 0,
            ))

            con.commit()

    def update_did_pay(self, did_pay=True):
        if not self.did_pay == did_pay:
            self.did_pay = did_pay
            value = 1 if did_pay else 0
            with sqlite3.connect(database_file) as con:
                cursor = con.cursor()
                cursor.execute("UPDATE reservations SET did_pay={} WHERE event_id='{}'".format(value, self.event_id))
                con.commit()

    def add_event(self, calendar):
        place = self.get_place()
        self.event_id = calendar.add_event(self.event_name, place, self.start_time, self.end_time)

    def add(self, calendar):
        self.add_event(calendar)
        self.add_record()

    def delete_record(self):
        with sqlite3.connect(database_file) as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM reservations where event_id='{}'".format(self.event_id))
            con.commit()

    def delete_event(self, calendar):
        calendar.delete_event(self.get_place(), self.event_id)

    def delete(self, calendar):
        try:
            self.delete_event(calendar)
        except:
            pass
        self.delete_record()

    def get_place(self):
        return "lounge" if self.place_id is 0 else "bbq"

    def render_time(self, isStart=True):
        if isStart:
            return self.start_time.strftime("%m-%d-%Y %I:%M %p")
        else:
            return self.end_time.strftime("%m-%d-%Y %I:%M %p")

    def send_confirmation(self):
        name = "{} {}".format(self.first_name, self.last_name) 
        to = "{} <{}>".format(name, self.email)
        place = "Lounge" if self.place_id is 0 else "BBQ"
        subject = "{} Reservation Confirmation ({})".format(place, self.event_name)

        starts = self.render_time()

        message = \
        """ 
        Hi {},
        This is a reminder email of your {} reservation starting {}

        Please make sure you review the {} rules.
        *** THERE IS A $60 FINE FOR LEAVING THE PLACE MESSY***
        
        """.format(self.first_name, place, starts, place)

        send_mail(sender = admin_email, proxy = admin_email, to = to, cc = admin_email, subject = subject, text = message);
        
    def get_obj(self):
        obj = vars(self)

        obj['alcohol'] = "serving, guests more than 50"

        if self.alcohol_type is 0:
            obj['alcohol'] = "not serving alcohol"
        elif self.alcohol_type is 1:
            obj['alcohol'] = "serving, guests equal or less than 50"
        obj['name'] = "{} {}".format(self.first_name, self.last_name)
        obj['place'] = "Lounge" if self.place_id is 0 else "BBQ"
        obj['hundred'] = "No" if self.is_hundred_or_more is 0 else "Yes"
        obj['starts'] = self.start_time.strftime("%Y-%m-%d %I:%M %p")
        obj['ends'] = self.end_time.strftime("%Y-%m-%d %I:%M %p")
        
        return obj

    def to_json(self):
        d = vars(self)
        d['start_time'] = self.start_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        d['end_time'] = self.end_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        return json.dumps(d)
