#!/usr/bin/python

import cgitb;cgitb.enable()
import lib,cgi

if not lib.IsSecure():
    lib.SecureRedirect()
else:
    if not lib.SuperAuth():
        print 'Content-type: text/html'
        print
        print lib.noauth
    else:
        form = cgi.FieldStorage()
        Get = lambda x:lib.Get(x,form,default='False')
        credit = lib.File2Param(lib.freedb,'d').copy()
        for office in lib.officers.keys():
            w = Get(office)
            try:
                w = int(w)
                credit[office] = w
            except:
                pass
        lib.Param2File(credit,lib.freedb)
    lib.Redirect(lib.admin)          
            
