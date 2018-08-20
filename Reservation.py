import os
from datetime import datetime
import json

class Reservation:

    @staticmethod
    def setup_database(cursor):
        os.environ['TZ'] = 'America/New_York'
        cursor.execute("CREATE TABLE IF NOT EXISTS reservations ( \
             id INTEGER PRIMARY KEY, \
             first_name TEXT, \
             last_name TEXT, \
             email TEXT, \
             apartment, TEXT, \
             place_id INTEGER, \
             event_name TEXT, \
             admitOne TEXT, \
             start_time INTEGER, \
             end_time INTEGER, \
             is_wec INTEGER, \
             is_hundred_or_more INTEGER, \
             alcohol_type INTEGER);")

    @staticmethod
    def select_all(cursor):
        cursor.execute("SELECT * FROM reservations")
        return cursor.fetchall()

    def __init__(self, first_name, last_name, email, apartment, place_id, event_name, adMitOne, date, starts, ends, is_wec, is_hundred_or_more, alcohol_type):
        
        print(datetime.strptime("{} {}".format(date, starts), "%Y-%m-%d %H:%M").tzinfo())
        print(datetime.strptime("{} {}".format(date, ends), "%Y-%m-%d %H:%M"))

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.apartment = apartment
        self.place_id = place_id
        self.event_name = event_name
        self.adMitOne = adMitOne
        self.start_time = 0
        self.end_time = 0
        self.is_wec = is_wec
        self.is_hundred_or_more = is_hundred_or_more
        self.alcohol_type = alcohol_type

    def add_record(self, cursor):
        cursor.execute("INSERT INTO reservations (first_name, last_name, email, apartment, place, event_name, adMitOne, start_time, end_time, is_wec, is_hundred_or_more, alcohol_type) VALUES ('{fn}', '{ln}', '{em}', '{ap}', {pl}, '{en}', '{ad}', {st}, {et}, {iw}, {ih}, {at})".format(
            fn = self.first_name,
            ln = self.last_name,
            em = self.email,
            ap = self.apartment,
            pl = self.place_id,
            en = self.event_name,
            ad = self.adMitOne,
            st = self.start_time,
            et = self.end_time,
            iw = self.is_wec,
            ih = self.is_hundred_or_more,
            at = self.alcohol_type
            ))

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
        
        return obj


    def to_json(self):
        return json.dumps(vars(self))
