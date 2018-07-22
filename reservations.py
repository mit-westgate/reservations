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

# import sqlite3
# conn = sqlite3.connect('reservations.db')

###############################################################################
def index():
    return render_template('index.html')

def confirm():
    return render_template('confirm.html')

def success():
    return render_template('success.html')

def admin():
    return render_template('admin.html')

###############################################################################
app = Flask(__name__, template_folder='./templates', static_url_path='/static')
app.debug = True
app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/confirm', 'confirm', confirm, methods=['GET'])
app.add_url_rule('/success', 'success', success, methods=['GET'])
app.add_url_rule('/admin', 'admin', admin, methods=['GET'])

@app.after_request
def disable_xss_protection(response):
    response.headers.add('X-XSS-PROTECTION', '0')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')

