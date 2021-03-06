from localization import *
from html import *
from mlhtml import *
from mlutils import *
from mllist import *
from mlemail import *

FROM = TITLE + '<noreply@' + DOMAIN + '>'

def EmailNewPhoto(filename,pid,id):
  dict = {}
  dict['id']    = id
  #dict['image'] = ImageData(filename)
  dict['filename'] = PhotoFilename(pid)

  html = RenderY('email-new-photo.html', dict)
  Email2(FROM, ['keith.hollis@gmail.com'], 'New Photo Uploaded (%d)' % (pid), html, 10)

def EmailVerify(email,id):
  dict = {}
  dict['id']    = id
  dict['email'] = email

  html = RenderY('email-verify.html', dict)
  Email2(FROM, [email], 'Verify Registration', html, 1)

def EmailPassword(email,password):
  dict = {}
  dict['password'] = password

  html = RenderY('email-password.html', dict)
  Email2(FROM, [email], 'Password Reminder', html, 1)

def EmailKicked(email):
  dict = {}

  html = RenderY('email-kicked.html', dict)
  Email2(FROM, [email], 'Removal Alert', html)

def EmailKickedStopForumSpam(email):
  dict = {}

  html = RenderY('email-kicked-stopforumspam.html', dict)
  Email2(FROM, [email], 'Removal Alert', html)

def EmailPhotoDeleted(email):
  dict = {}

  html = RenderY('email-photo-deleted.html', dict)
  Email2(FROM, [email], 'Photo Removal Alert', html)

def EmailWink(entry,entry_from):
  email    = entry[COL_EMAIL]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  tz       = entry[COL_TZ]
  adjust = GazLatAdjust(entry_from[COL_Y])
  dx = abs(entry_from[COL_X]-entry[COL_X])*adjust/1000
  dy = abs(entry_from[COL_Y]-entry[COL_Y])/1000
  distance = math.sqrt((dx*dx)+(dy*dy))

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['action']     = 'emailthread'
  dict['navigation'] = 'inbox'

  member = {}
  member['id']            = entry_from[COL_ID]
  member['image']         = PhotoFilename(MasterPhoto(entry_from[COL_ID]))
  member['name']          = mask.MaskEverything(entry_from[COL_NAME])
  member['gender']        = Gender(entry_from[COL_GENDER])
  member['age']           = Age(entry_from[COL_DOB])
  member['starsign']      = Starsign(entry_from[COL_DOB])
  member['ethnicity']     = Ethnicity(entry_from[COL_ETHNICITY])
  member['location']      = entry_from[COL_LOCATION]
  member['summary']       = mask.MaskEverything(entry_from[COL_SUMMARY])
  member['last_login']    = Since(entry_from[COL_LAST_LOGIN])
  member['login_country'] = entry_from[COL_LAST_IP_COUNTRY]
  member['created']       = Datetime(entry_from[COL_CREATED2], tz).strftime('%x')
  member['distance']      = Distance(distance, unit_distance)
  member['active']        = False
  dict['entry'] = member

  html = RenderY('email-wink.html', dict)
  Email2(FROM, [email], 'New Wink! Received', html)

def EmailNotify(entry,entry_from):
  email    = entry[COL_EMAIL]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  tz       = entry[COL_TZ]
  adjust = GazLatAdjust(entry_from[COL_Y])
  dx = abs(entry_from[COL_X]-entry[COL_X])*adjust/1000
  dy = abs(entry_from[COL_Y]-entry[COL_Y])/1000
  distance = math.sqrt((dx*dx)+(dy*dy))

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['action']     = 'emailthread'
  dict['navigation'] = 'inbox'

  member = {}
  member['id']            = entry_from[COL_ID]
  member['image']         = PhotoFilename(MasterPhoto(entry_from[COL_ID]))
  member['name']          = mask.MaskEverything(entry_from[COL_NAME])
  member['gender']        = Gender(entry_from[COL_GENDER])
  member['age']           = Age(entry_from[COL_DOB])
  member['starsign']      = Starsign(entry_from[COL_DOB])
  member['ethnicity']     = Ethnicity(entry_from[COL_ETHNICITY])
  member['location']      = entry_from[COL_LOCATION]
  member['summary']       = mask.MaskEverything(entry_from[COL_SUMMARY])
  member['last_login']    = Since(entry_from[COL_LAST_LOGIN])
  member['login_country'] = entry_from[COL_LAST_IP_COUNTRY]
  member['created']       = Datetime(entry_from[COL_CREATED2], tz).strftime('%x')
  member['distance']      = Distance(distance, unit_distance)
  member['active']        = False
  dict['entry'] = member

  html = RenderY('email-notify.html', dict)
  Email2(FROM, [email], 'New Message Received', html)

def EmailNewMembers(entry,ids):
  email    = entry[COL_EMAIL]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['action']     = 'member'
  dict['navigation'] = 'matches'
  dict['entries'] = ListMembers(ids,None,location,x,y,tz,unit_distance)

  html = RenderY('email-newmembers.html', dict)
  Email2(FROM, [email], 'New Members Available', html, 4)

def EmailInboxReminder(email,name):
  dict = {}
  dict['name'] = name

  html = RenderY('email-inbox-reminder.html', dict)
  Email2(FROM, [email], 'Unread Messages Reminder', html, 1)
