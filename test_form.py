#!/usr/bin/python

import cgitb;cgitb.enable()
import lib
import os

e=os.environ
print 'Content-type: text/html'
print
#print lib.noauth
print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>No Authorization</title>
 </head>
 <body>
   <h3>
    No Authorization
   </h3>
   <hr>
   %(envir)s
 </body>
</html>
""" % {'envir':e}
