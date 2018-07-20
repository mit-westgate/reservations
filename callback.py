#!/usr/bin/python

import cgi
form = cgi.FieldStorage()

print "Content-Type: text/plain"
print
print "hello"
print form["username"].value
