#!/usr/bin/python

import cgitb;cgitb.enable()
import lib

def CreditHtml(office,credit):
    return \
"""
<tr>
 <td>%(office)s</td>
 <td><input type="text" value="%(credit)s" name="%(office)s" class="credit w77"></td>
</tr>
""" % {'office':office,'credit':credit}

def ViewCreditHtml(office,credit):
    return \
"""
<tr>
 <td>%(office)s</td>
 <td><input type="text" value="%(credit)s" name="%(office)s" class="credit w77" disabled></td>
</tr>
""" % {'office':office,'credit':credit}

if not lib.IsSecure():
    lib.SecureRedirect()
else:
    if not lib.OfficerAuth() and not lib.SuperAuth():
        print 'Content-type: text/html'
        print
        print lib.noauth
    elif lib.SuperAuth():
        credit = lib.File2Param(lib.freedb,'d')
        credlist = ''.join([CreditHtml(o,c) for o,c in credit.items()])
        credtext = \
"""
<h3>Officer Reservation Waivers</h3>
<hr>
<form method="post" action="%(credit)s">
 <table>
  %(credlist)s
 </table>
 <div class="submit">
  <input type="submit" value="Submit">
 </div>
</form>
""" % {'credlist':credlist,'credit':lib.credit}
        print 'Content-type: text/html'
        print
        print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Reservation Administration</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
  <script language="javascript" type="text/javascript">
   function enterdates() {
    var now = new Date();
    var t0 = new Date();
    var t1 = new Date();
    t0.setDate(now.getDate()-30);
    t1.setDate(now.getDate()+30);
    document.form.dstart.value = (t0.getMonth()+1)+'-'+t0.getDate()+'-'+checkYear(t0.getYear());
    document.form.dend.value = (t1.getMonth()+1)+'-'+t1.getDate()+'-'+checkYear(t1.getYear());
    document.form.unpaid.checked = true;
    document.form.paid.checked = false;
    document.form.user.focus();
   }
   function checkYear(y) {
    if (y < 2000) y += 1900;
    return (y);
   }
  </script>
 </head>
 <body onload="enterdates()">
  <div id="main">
   <h3>
    Reservation Administration
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
   </h3>   
   <hr>
   <form name="form" method="get" action="%(table)s">
    <table class="inptab">
     <tr>
      <td class="head">Start Date</td>
      <td><input type="text" name="dstart" size=30></td>
     </tr>
     <tr>
      <td class="head">End Date</td>
      <td><input type="text" name="dend" size=30></td>
     </tr>
     <tr>
      <td class="head"><input type="checkbox" name="unpaid" value="True"></td>
      <td>Display unpaid events</td>
     </tr>
     <tr>
      <td class="head"><input type="checkbox" name="paid" value="True"></td>
      <td>Display paid events</td>
     </tr>
    </table>
    <div class="submit">
     <input type="submit" value="Submit">
    </div>
   </form>
   %(credtext)s
  </div>
 </body>
</html>
""" % {'css':lib.css,'table':lib.table,'main':lib.main,'form':lib.form, \
       'credtext':credtext}
    else:
        credit = lib.File2Param(lib.freedb,'d')
        credlist = ''.join([ViewCreditHtml(o,c) for o,c in credit.items()])
        credtext = \
"""
<table>
 %(credlist)s
</table>
""" % {'credlist':credlist,'credit':lib.credit}
        print 'Content-type: text/html'
        print
        print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Reservation Administration</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    Officer Reservation Waivers
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
   </h3>   
   <hr>
   %(credtext)s
  </div>
 </body>
</html>
""" % {'css':lib.css,'main':lib.main,'form':lib.form, \
       'credtext':credtext}