#!/usr/bin/python

import cgitb;cgitb.enable()
import lib

if not lib.IsSecure():
    lib.SecureRedirect()
else:
    credit = lib.GetCredit()
    if credit != None and  credit >= lib.costperblk:
        free = \
"""
<tr>
 <td class="head"><input type="checkbox" name="free" value="True"></td>
 <td>
  <div class="w370">
   As a Westgate officer, I want to waive this reservation fee. I have
   $%(credit)s of reservation credit remaining.
  </div>
 </td>
</tr>
""" % {'credit':credit}
    else:
        free = ''

    if lib.OfficerAuth() or lib.SuperAuth():
        sponsor = \
"""
<tr>
 <td class="head"><input type="checkbox" name="wec" value="True"></td>
 <td>
  <div class="w370">
   This event is sponsored by the Westgate Executive Committee
  </div>
 </td>
</tr>
"""
    else:
        sponsor = ''

    print 'Content-type: text/html'
    print
    print \
"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
 <head>
  <title>Westgate Reservations</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
  <script language="javascript" type="text/javascript">
   function entertext(id) {
    var e = document.getElementById(id);
    es = e.className;
    if (/ inactive/.test(es)) {
     e.className = es.replace(/ inactive/g,' active');
     e.value = '';
    }
   }
   function exittext(id) {
    var e = document.getElementById(id);
    var val = e.value;
    if (/^(\s*)$/.test(val)) {
     e.className = e.className.replace(/ active/g,' inactive');
     e.value = e.getAttribute('ghost');
    }
   }
   function initialfields() {
    var e = document.getElementById('form');
    for (var i=0;i<e.length;i++) {
     if (e[i].id) {
      var val = e[i].value;
      es = e[i].className;
      if ((/^(\s*)$/.test(val) || val == e[i].getAttribute('ghost')) && !/child/.test(e[i].id)) {
       e[i].className = es.replace(/ active/g,' inactive');
       e[i].value = e[i].getAttribute('ghost');
      } else
       e[i].className = es.replace(/ inactive/g,' active')
     }
    }
   }
   function clearfields() {
    var e = document.getElementById('form');
    for (var i=0;i<e.length;i++) if (/ inactive/.test(e[i].className)) e[i].value = '';
   }
  </script>
 </head>
 <body onload="initialfields()">
  <div id="main">
   <h3>
    <p class="left">
     Westgate Reservations
     &#183; <a href="%(main)s">Westgate Home</a>
    </p>
    <p class="right">
     <a href="%(admin)s">Admin</a>
     <a href="%(test)s">Test</a>
    </p>
    <div class="clear"></div>
   </h3>
   <hr>
   After viewing the online <a href="%(lngcal)s">lounge</a> or
   <a href="%(bbqcal)s">barbecue</a> calendar and finding an open time
   slot, complete the form below to request a reservation for the Westgate
   lounge or barbecue area. Upon registration, a temporary reservation will
   appear on the appropriate calendar. Pay the reservation fee ($10 per 4-hour
   block) to the %(money_collect_name)s at apartment %(money_collect_room)s to finalize
   the transaction and make a permanent reservation.
   <br/>
   <br/>
   <b>
   For barbecue reservations, make sure you read carefully the MIT safety guidelines.
   <a href="https://ehs.mit.edu/site/content/barbecue-safety-guidelines"
      target="_blank">
      https://ehs.mit.edu/site/content/barbecue-safety-guidelines</a>
    </b>
   <form name="form" id="form" method="post" action="%(process)s" onsubmit="clearfields()">
    <h3>Personal & Event Information</h3>
    <hr>
    <table id="formtable">
     <tr>
      <td class="head">Title</td>
      <td>
       <select name="ntitle">
        <option selected value="Mr.">Mr.</option>
        <option value="Mrs.">Mrs.</option>
        <option value="Ms.">Ms.</option>
        <option value="Miss">Miss</option>
        <option value="Dr.">Dr.</option>
       </select>
      </td>
     </tr>
     <tr>
      <td class="head">Given Name</td>
      <td><input type="text" name="gname" class="w314"></td>
     </tr>
     <tr>
      <td class="head">Family Name</td>
      <td><input type="text" name="fname" class="w314"></td>
     </tr>
     <tr>
      <td class="head">Apartment</td>
      <td><input type="text" name="apt" class="w314"></td>
     </tr>
     <tr>
      <td class="head">Daytime Phone</td>
      <td><input type="text" name="dfone" class="w314"></td>
     </tr>
     <tr>
      <td class="head">Evening Phone</td>
      <td><input type="text" name="efone" class="w314"></td>
     </tr>
     <tr>
      <td class="head">E-mail Address</td>
      <td><input type="text" name="email" class="w314"></td>
     </tr>
     <tr>
      <td class="head">Event Title</td>
      <td><input type="text" name="etitle" class="w314"></td>
     </tr>
     <tr>
      <td class="head">Reservation Area</td>
      <td>
       <input type="radio" name="area" value="%(name1)s">Lounge
       <input type="radio" name="area" value="%(name2)s">Barbecue
      </td>
     </tr>
     <tr>
      <td class="head">Event Date</td>
      <td><input type="text" name="date" id="date" class="w314 inactive" ghost="mm/dd/yyyy" onfocus="entertext(this.id)" onblur="exittext(this.id)"></td>
     </tr>
     <tr>
      <td class="head">Start Time</td>
      <td><input type="text" name="tstart" id="tstart" class="w314 inactive" ghost="hh:mm am/pm" onfocus="entertext(this.id)" onblur="exittext(this.id)"></td>
     </tr>
     <tr>
      <td class="head">End Time</td>
      <td><input type="text" name="tend" id="tend" class="w314 inactive" ghost="hh:mm am/pm" onfocus="entertext(this.id)" onblur="exittext(this.id)"></td>
     </tr>
     %(sponsor)s
     %(free)s
     <tr>
      <td class="head"><input type="checkbox" name="agree" value="True"></td>
      <td>
       <div class="w370">
        I have read and agree with the <a href="%(lngrule)s">lounge</a> or
        <a href="%(bbqrule)s">barbecue</a> rules, including the fact of a  <strong>$60 fine</strong> if the place is left messy.
       </div>
      </td>
     </tr>
     <tr>
      <td colspan="2" class="head2">
       Will 100 or more guests be at this event?
      </td>
     </tr>
     <tr>
      <td class="head"><input type="radio" name="size" value="small"></td>
      <td>
       <div class="w370">
        No.
       </div>
      </td>
     </tr>
     <tr>
      <td class="head"><input type="radio" name="size" value="large"></td>
      <td>
       <div class="w370">
        Yes. I will file all of the necessary forms prior to the event and comply with all MIT policies found on
        the <a href="%(eventreg)s">MIT Event Registration Form</a>.
       </div>
      </td>
     </tr>
     <tr>
      <td colspan="2" class="head2">
       Will alcoholic beverages be at this event?
      </td>
     </tr>
     <tr>
      <td class="head"><input type="radio" name="alc" value="no"></td>
      <td>
       <div class="w370">
        No.
       </div>
      </td>
     </tr>
     <tr>
      <td class="head"><input type="radio" name="alc" value="yessmall"></td>
      <td>
       <div class="w370">
        Yes, and there will be 50 or fewer guests. I will file all necessary forms and comply with
        all alcohol-related policies found on the
        <a href="%(alcreg)s">Westgate Alcohol Registration Form</a>.
       </div>
      </td>
     </tr>
     <tr>
      <td class="head"><input type="radio" name="alc" value="yeslarge"></td>
      <td>
       <div class="w370">
        Yes, and there will be more than 50 guests. I will file all necessary forms and comply with
        all alcohol-related policies found at <a href="%(alcpolicy)s">Alcohol Policies and
        Procedures @ MIT</a> and on the <a href="%(eventreg)s">
        MIT Event Registration Form</a>.
       </div>
      </td>
     </tr>
    </table>
    <div class="submit">
     <input type="submit" value="Submit">
    </div>
   </form>
   <hr>
   <div class="footer">
    Questions or comments? Bugs? Contact the %(admin_name)s at <a href="mailto:%(admin_email)s">%(admin_email)s</a>.
   </div>
  </div>
 </body>
</html>
""" % {'css':lib.css,'process':lib.process,'lngcal':lib.lngcal,
       'bbqcal':lib.bbqcal,'lngrule':lib.lngrule,'bbqrule':lib.bbqrule, \
       'sponsor':sponsor,'name1':lib.names[0],'name2':lib.names[1], \
       'eventreg':lib.eventreg,'alcreg':lib.alcreg,'alcpolicy':lib.alcpolicy, \
       'main':lib.main,'admin':lib.admin,'free':free, 'admin_email':lib.admin_email,'admin_name':lib.admin_name,'money_collect_name':lib.money_collect_name, 'money_collect_room': lib.money_collect_room, 'test':lib.test_0612}
