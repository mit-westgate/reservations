#!/usr/bin/python

import cgitb;cgitb.enable()
import lib

print 'Content-type: text/html'
print
print \
"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
 <head>
  <title>Barbecue Area Reservation Rules</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    Barbecue Area Reservation Rules
   </h3>
   <hr>
   <p>
    The Westgate barbecue area is available to all Westgate residents for
    parties and other functions. The %(admin_name)s
    (<a href="mailto:%(admin_email)s">%(admin_email)s</a>) manage
    the reservation administration.
   </p>
   <h4>Reservations</h4>
   <ul>
    <li>
     The picnic area adjacent to the barbecue grills and the one grill closest
     to the tables are available for large parties or special events.
     Reservations are required for private parties, organized meetings, and
     other similar activities. Reservations may be made up to 30 days in
     advance. To make a reservation, complete the
     online reservation form at <a href="">%(form)s</a>.
    </li>
    <li>
     Reservations cost $%(cost)s per $%(time)s hours. Reservation fees should be
     paid with checks only (made out to MIT) and left in the drop box outside of
     the %(admin_name)s apartment (%(apt)s). Do not leave checks in or
     around the %(admin_name)s mailbox. Money collected from reservations
     will be deposited in Westgate's general account.
    </li>
    <li>
     Memorial Day (the last Monday in May), Independence Day (July 4th), and
     Labor Day (the first Monday in September) are three holidays during which
     the barbecue area is in high demand. To give all Westgate residents equal
     opportunity, barbecue area reservations are not allowed on these three
     holidays. Use of tables and grills will be on a first-come, first-served
     basis. Hopefully this policy maximizes use of the entire Westgate courtyard
     by residents' families and friends.
    </li>
    <li>
     Reservations may be cancelled at any time; however, the fee is forfeit if
     the reservations are cancelled less than a week in advance.
    </li>
    <li>
     All reservation requests are subject to the discretion of the Graduate
     Coordinators.
    </li>
   </ul>
   <h4>Barbecue Area Treatment</h4>
   <ul>
    <li>
     The individual making the reservation is responsible for the condition
     of the barbecue and its contents as well as the conduct of all guests. This
     individual is also financially responsible for all damages made, including
     those made by guests. Abuse of the barbecue area will result in a complete
     loss of reservation privileges.
    </li>
    <li>
     Coals must be extinguished before leaving.
    </li>
    <li>
     Put ashes into the metal can provided next to the grills. Do not put
     anything else into this can, such as other trash, paper plates, etc.
    </li>
    <li>
     Remember that this is your and everyone else's backyard. Clean up
     after yourselves.
    </li>
    <li>
     All trash must be brought to the trashrooms if the trascans outside
     are full.
    </li>
    <li>
     Please recycle all recyclable materials made from glass, plastic,
     aluminum, tin, steel, paper, etc. by putting them into the recycling bins
     behind the highrise building.
    </li>
    <li>
     The barbecue area curfew is midnight (12am).
    </li>
   </ul>
   <h4>Alcohol Policy</h4>
   <ul style="margin-top:0;padding-top:5px;margin-left:0;padding-left:20px">
    <li>
     If alcohol is to be present at a lounge event, it must be appropriately
     indicated on the online reservation form. The proper forms must also be
     filled out and submitted.
    </li>
    <li>
     If alcohol will be present and there will be 50 or fewer guests, the
     Westgate Alcohol Registration Form at <a href="">%(alcreg)s</a> must be
     completed and submitted to the House Manager's office in person, between
     8:30am and 3:30pm, Monday through Friday, at least 72 hours before the
     event.
    </li>
    <li>
     If alcohol will be present and there will be more than 50 guests, the
     MIT Event Registration Form at <a href="">%(eventreg)s</a> must be completed
     and submitted and all policies outlined at
     Alcohol Policies and Procedures @ MIT at <a href="">%(alcpolicy)s</a>
     must be understood and followed.
    </li>
  </div>
 </body>
</html>
""" % {'css':lib.css,'form':lib.form,'main':lib.main, \
       'cost':lib.costperblk,'time':lib.timeperblk,'apt':lib.admin_apt, \
       'alcreg':lib.alcreg,'alcpolicy':lib.alcpolicy, \
       'eventreg':lib.eventreg,'admin_email':lib.admin_email,'admin_name':lib.admin_name}
