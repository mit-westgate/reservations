#!/usr/bin/python
#: optional path to your local python site-packages folder
import sys
import os

main_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(main_dir, 'lib')
sys.path.insert(0, os.path.join(lib_dir, 'flup-1.0.2'))

# Append all packages in ./lib to path
for pkg in os.listdir(lib_dir):
    sys.path.insert(0, os.path.join(lib_dir, pkg))

## !/usr/bin/python
from flup.server.fcgi import WSGIServer
from reservations import app

# ------
class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'standalone':
        app.run(host='0.0.0.0')
    else:
        app = ScriptNameStripper(app)
        WSGIServer(app).run()
