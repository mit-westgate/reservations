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
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
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
      Reservations are subject to the MIT barbecue rules and safety guidelines.
      Please read carefully. 
      <a href="https://ehs.mit.edu/site/content/barbecue-safety-guidelines"
      target="_blank">
      https://ehs.mit.edu/site/content/barbecue-safety-guidelines</a>
    </li>
    <li>
     The picnic area adjacent to the barbecue grills and the one grill closest
     to the tables are available for large parties or special events.
     Reservations are required for planned parties, organized meetings, and
     other similar activities. Reservations may be made up to 30 days in
     advance. To make a reservation, complete the
     <a href="%(form)s">online reservation form</a>.
    </li>
    <li>
     Reservations cost $%(cost)s per %(time)s hours, and $0 if sign you up to volunteer for "Grill Night". Reservation fees should be
     paid with checks only (made out to MIT) and left in the drop box outside of
     the %(money_collect_name)s apartment (%(money_collect_room)s, <a href="%(map)s">map
     here</a>). Do not leave checks in or
     around the %(money_collect_name)s mailbox. Money collected from reservations
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
    <li>
     <span style="color:red">If the BBQ Area is found to be messy and/or full of garbage after your event, you will be charged a $60 FINE.</style>
    </li>
   </ul>
   <h4>Alcohol Policy</h4>
   <ul>
    <li>
     If alcohol is to be present at an event in the barbecue area, it must
     be appropriately indicated on the online reservation form. The proper
     forms must also be filled out and submitted (see below).
    </li>
    <li>
     If alcohol will be present and there will be 50 or fewer guests, the
     <a href="%(alcreg)s">Westgate Alcohol Registration Form</a> must be
     completed and submitted to the House Manager's office in person, between
     8:30am and 3:30pm, Monday through Friday, at least 72 hours before the
     event.
    </li>
    <li>
     If alcohol will be present and there will be more than 50 guests, the
     <a href="%(eventreg)s">MIT Event Registration Form</a> must be completed
     and submitted and all policies outlined at
     <a href="%(alcpolicy)s">Alcohol Policies and Procedures @ MIT</a> must be
     understood and followed.
    </li>
  </div>
 </body>
</html>
""" % {'css':lib.css,'form':'https://westgate.mit.edu:444/scripts/reservations/form.py','main':lib.main, \
       'cost':lib.costperblk,'time':lib.timeperblk, \
       'alcreg':lib.alcreg,'alcpolicy':lib.alcpolicy, \
       'money_collect_name':lib.money_collect_name,'money_collect_email':lib.money_collect_email,'money_collect_room':lib.money_collect_room, \
       'eventreg':lib.eventreg,'map':lib.admin_map_url,'admin_email':lib.admin_email,'admin_name':lib.admin_name}
