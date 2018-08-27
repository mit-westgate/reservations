#!/usr/bin/python

import sys
import os

main_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(main_dir, 'lib')

# Append all packages in ./lib to path
for pkg in os.listdir(lib_dir):
    sys.path.insert(0, os.path.join(lib_dir, pkg))

# TODO: cherry pick what I need...

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environemnt(
        loader = PackageLoader('resevations', 'templates'),
        autoescape = select_autoescape(['html', 'xml'])
)


template = env.get_template("admin.html")
print template.render()
