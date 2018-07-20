#!/usr/bin/python

from jinja2 import FileSystemLoader, Template, select_autoescape
from os.path import abspath, dirname, join


current_dir = dirname(os.path.abspath(__file__))

env = Enviroment(
        loader = FileSystemLoader(join(current_dir, 'templates'))
        autoescape=select_autoescate(['html','xml'])
)

template = Template('Hello {{ name }}')

print "Content-type: text/html\n"
print "<html>hello world.</html>"

print template.render(name='me')
