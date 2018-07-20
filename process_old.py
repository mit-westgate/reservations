#!/usr/bin/python

import cgitb;cgitb.enable()
import lib,cgi

if not lib.IsSecure():
    lib.SecureRedirect()
else:
    form = cgi.FieldStorage()
    p = lib.ProcessForm(form)
    if len(p['errors']) > 0:
        errors = '<ul>\n<li>'+'</li>\n<li>'.join(p['errors'])+'</li>\n</ul>'
        print 'Content-type: text/html'
        print
        print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Westgate Reservations Error</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    User Error
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
   </h3>
   <hr>
   Your form submission generated the following errors and warnings.
   Please go back and try again.
   %(errors)s
  </div>
 </body>
</html>
""" % {'css':lib.css,'errors':errors,'form':lib.form,'main':lib.main}
    else:
        startstr = lib.Goog2Str(p['start'])
        endstr = lib.Goog2Str(p['end'])
        p['wecbool'] = str(p['wec'])
        p['wecstr'] = p['wec']*'Yes'+((not p['wec'])*'No')
        p['main'] = lib.main
        p['form'] = lib.form
        sizehtml = (p['size'] == 'large')* \
"""
<tr>
 <td class="head">Large Event Policy</td>
 <td>
  <div class="w370">
   There will be 100 or more guests at this event. I will file all necessary
   forms and comply with all policies found on the
   <a href="%(eventreg)s">MIT Event Registration Form</a>.
  </div>
 </td>
</tr>
""" % {'eventreg':lib.eventreg}
        alchtml = (p['alc'] == 'yessmall')* \
"""
<tr>
 <td class="head">Alcohol Policy</td>
 <td>
  <div class="w370">
   Alcohol will be at this event and there will be 50 or fewer
   guests. I will file all necessary forms and comply with all
   policies found on the <a href="%(alcreg)s">Westgate Alcohol Registration
   Form</a>.
  </div>
 </td>
</tr>
""" % {'alcreg':lib.alcreg}+(p['alc'] == 'yeslarge')* \
"""
<tr>
 <td class="head">Alcohol Policy</td>
 <td>
  <div class="w370">
   Alcohol will be at this event and there will be more than 50
   guests. I will file all necessary forms and comply with all
   policies found at <a href="%(alcpolicy)s">Alcohol Policies and Procedures
   @ MIT</a> and on the <a href="%(eventreg)s">MIT Event Registration
   Form</a>.
  </div>
 </td>
</tr>
""" % {'alcpolicy':lib.alcpolicy,'eventreg':lib.eventreg}
        if p['free'] and not p['wec']:
            payhtml = \
"""
I confirm the above information. As a Westgate officer, I want to waive the
fee of $%(cost)s for my %(dt)s-hour reservation and instead deduct it from my
$%(credit)s of credit.
""" % p
        else:
            if p['wec']:
                payhtml = \
"""
I confirm the above information. Because this event is sponsored by the
Westgate Executive Committee, the fee of $%(cost)s for my %(dt)s-hour
reservation will be waived.
""" % p
            else:
                payhtml = \
"""
I confirm the above information and I confirm that I will pay $%(cost)s for
my %(dt)s-hour reservation.
""" % p
        p.update({'css':lib.css,'startstr':startstr,'endstr':endstr, \
                  'fee':lib.costperblk,'time':lib.timeperblk, \
                  'sizehtml':sizehtml,'alchtml':alchtml, \
                  'payhtml':payhtml,'confirm':lib.confirm})
        print 'Content-type: text/html'
        print
        print \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Westgate Reservations Confirmation</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    Event Confirmation
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
   </h3>
   <hr>
   Please review your event details below and confirm both that the information
   shown is correct and that you are willing to pay the reservation fee.
   Reservations cost $%(fee)s for a %(time)s-hour time block.
   <h3>Reservation Details</h3>
   <hr>
   <table>
    <tr>
     <td class="head">Name</td>
     <td>%(ntitle)s %(gname)s %(fname)s</td>
    </tr>
    <tr>
     <td class="head">Apartment</td>
     <td>%(apt)s</td>
    </tr>
    <tr>
     <td class="head">Daytime Phone</td>
     <td>%(dfone)s</td>
    </tr>
    <tr>
     <td class="head">Evening Phone</td>
     <td>%(efone)s</td>
    </tr>
    <tr>
     <td class="head">E-mail Address</td>
     <td><a href="mailto:%(email)s">%(email)s</a></td>
    </tr>
    <tr>
     <td class="head">Event Title</td>
     <td>%(etitle)s</td>
    </tr>
    <tr>
     <td class="head">Reservation Area</td>
     <td>%(area)s</td>
    </tr>
    <tr>
     <td class="head">Event Start</td>
     <td>%(startstr)s</td>
    </tr>
    <tr>
     <td class="head">Event End</td>
     <td>%(endstr)s</td>
    </tr>
    <tr>
     <td class="head">WEC Sponsored</td>
     <td>%(wecstr)s</td>
    </tr>
    %(sizehtml)s
    %(alchtml)s
   </table>
   <h3>Payment Confirmation</h3>
   <hr>
   <form method="post" action="%(confirm)s">
    <table>
     <tr>
      <td class="head">
       <input type="checkbox" name="pay" value="True">
      </td>
      <td>
       <div class="w370">
        %(payhtml)s
       </div>
      </td>
     </tr>
    </table>
    <div class="submit">
     <input type="submit" value="Submit">
    </div>
    <input type="hidden" name="ntitle" value="%(ntitle)s">
    <input type="hidden" name="gname" value="%(gname)s">
    <input type="hidden" name="fname" value="%(fname)s">
    <input type="hidden" name="apt" value="%(apt)s">
    <input type="hidden" name="dfone" value="%(dfone)s">
    <input type="hidden" name="efone" value="%(efone)s">
    <input type="hidden" name="email" value="%(email)s">
    <input type="hidden" name="etitle" value="%(etitle)s">
    <input type="hidden" name="area" value="%(area)s">
    <input type="hidden" name="date" value="%(date)s">
    <input type="hidden" name="tstart" value="%(tstart)s">
    <input type="hidden" name="tend" value="%(tend)s">
    <input type="hidden" name="wec" value="%(wecbool)s">
    <input type="hidden" name="free" value="%(free)s">
    <input type="hidden" name="agree" value="%(agree)s">
    <input type="hidden" name="size" value="%(size)s">
    <input type="hidden" name="alc" value="%(alc)s">
   </form>
  </div>
 </body>
</html>
""" % p
