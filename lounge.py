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
  <title>Lounge Reservation Rules</title>
  <link rel="stylesheet" href="%(css)s" type="text/css">
 </head>
 <body>
  <div id="main">
   <h3>
    Lounge Reservation Rules
    &#183; <a href="%(form)s">Reservation Application</a>
    &#183; <a href="%(main)s">Westgate Home</a>
   </h3>
   <hr>
   <p>
    The Westgate lounge is available to all Westgate residents for parties
    and other functions. The %(admin_name)ss
    (<a href="mailto:%(admin_email)s">%(admin_email)s</a>) manage
    the reservation administration.
   </p>
   <h4>Reservations</h4>
   <ul>
    <li>
     Reservations are required for private parties, organized meetings, and
     other similar activities. Reservations may be made up to 30 days in
     advance. To make a reservation, complete the
     <a href="%(form)s">online reservation form</a>.
    </li>
    <li>
     Reservations cost $%(cost)s per %(time)s hours. Reservation fees should be
     paid with checks only (made out to MIT) and left in the drop box outside of
     the %(money_collect_name)s apartment (%(money_collect_room)s, <a href="%(map)s">map
     here</a>). Do not leave checks in or
     around the %(money_collect_name)s mailbox. Money collected from reservations
     will be deposited in Westgate's general account for use in lounge maintenance
     and other needs.
    </li>
    <li>
     Reservations may be cancelled at any time; however, the fee is still required
     if the reservations are cancelled less than a week in advance. Contact the
     %(admin_name)s at (<a href="mailto:%(admin_email)s">%(admin_email)s</a>)
     to cancel your reservation.
    </li>
    <li>
     Lounge reservations for weekend evenings (5pm-12am) are usually highly
     sought after. In an effort to evenly distribute these reservation times,
     lounge policy dictates that each resident or group may only reserve one
     weekend evening reservation per month (even if the group includes multiple
     Westgate residents). If a weekend evening is still available five days
     in advance (e.g., as of Sunday, a Friday evening is still open on the
     calendar) any individual or group is allowed to reserve that weekend
     evening, regardless of other reservations they may have that month.
    </li>
    <li>
     Payments must be made within two weeks of placing the reservation.
    </li>
    <li>
     Residents cannot make a new reservation until all past unpaid reservations
     have been paid. Failure to pay could result in loss of lounge reservation
     privileges until all money has been received.
    </li>
    <li>
     Reservations can only be made by Westgate Residents. Other MIT affiliates
     do not have access to the building, and therefore are unable to reserve
     the lounge.
    </li>
    <li>
     All reservation requests are subject to the discretion of the Graduate
     Coordinators.
    </li>
   </ul>
   <h4>Lounge Treatment</h4>
   <ul>
    <li>
     The individual making the reservation is responsible for the condition
     of the lounge and its contents as well as the conduct of all guests. This
     individual is also financially responsible for all damages made to lounge
     property, including damages or abuse done by guests. The individual is
     responsible for damages up to the full cost of property replacement,
     including those made by guests. Abuse of the lounge will result in a
     complete loss of reservation privileges.
    </li>
    <li>
     Smoking is not permitted in the lounge. There is no external ventilation
     in this room, and it is used by the entire Westgate community.
    </li>
    <li>
     Arrangements must be made to admit guests into the building. Blocking or
     propping doors external to the building is a security breach and is
     absolutely not permitted.
    </li>
   </ul>
   <h4>Cleaning</h4>
   <ul>
    <li>
     The individual who made the reservation is responsible for the cleanliness
     of the lounge after their reservation is complete. The lounge must be
     entirely clean by the end of the reservation time, so plan accordingly.
     The individual who made the reservation is responsible to provide their
     own cleaning supplies. If you do not own a vacuum, one is available for
     use at the Tang Front Desk. Make accommodations ahead of time to allow
     yourself to properly clean the lounge.
    </li>
    <li>
     Failure to properly clean the lounge after your reservation can result
     in a fine of $40. If there is another event planned after yours, make
     sure you have properly cleaned so you are not held responsible for any
     of their mess.
     <ul>
      <li>
       If you are fined you will have 1 week to pay the $40 fine by check.
       If you do not pay by then it will be charged to your Student Bursar
       Account, with an additional $10 as a late fee (total of $50).
      </li>
      <li>
       If you disagree with the fine, you can go through an appeal process,
       but this does not guarantee the fee will be waived.
      </li>
     </ul>
    </li>
    <li>
     Any Westgate resident can be fined for not leaving the lounge in clean
     and orderly condition after their use, even if they have not reserved
     the lounge.
    </li>
    <li>
     Properly cleaning the lounge includes:
     <ul>
      <li>
       Wipe all tables and countertops with a clean, damp cloth.
      </li>
      <li>
       Wipe down the furniture with a slightly damp cloth.
      </li>
      <li>
       Vacuum the carpeted area and sweep the kitchen floor, mopping up all
       spills with a clean, damp mop after sweeping.
      </li>
      <li>
       Rinse out the sink.
      </li>
      <li>
       Clean spills in the oven and on the stovetop.
      </li>
      <li>
       Empty and clean the refrigerator and freezer.
      </li>
      <li>
       Empty and replace all full garbage cans and recycling bins and replace
       with a new trash liner (found in trash rooms). Place trashbags in a
       trash room or the Tang dumpsters.
      </li>
     </ul>
    </li>
   </ul>
   <h4>Alcohol Policy</h4>
   <ul>
    <li>
     If alcohol is to be present at a lounge event, it must be appropriately
     indicated on the online reservation form. The proper forms must also be
     filled out and submitted (see below).
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
       'admin_name':lib.admin_name,'admin_email':lib.admin_email, \
       'money_collect_name':lib.money_collect_name,'money_collect_email':lib.money_collect_email,'money_collect_room':lib.money_collect_room, \
       'alcreg':lib.alcreg,'alcpolicy':lib.alcpolicy, \
       'eventreg':lib.eventreg,'map':lib.admin_map_url,'admin_email':lib.admin_email,'admin_name':lib.admin_name}
