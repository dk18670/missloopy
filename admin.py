#!/usr/bin/python

import sys, optparse, re, mask

import database2

from iputils import *
from mlutils import *

parser = optparse.OptionParser()
parser.add_option("-n", "--non-interactive", dest="stdin", action="store_true", help="use stdin for input")

(options, args) = parser.parse_args()

db = database2.Database(MISS_LOOPY_DB)

def command(cmd):
  cmds = cmd.strip().upper().split()
  if len(cmds) == 0:
    return
  n = 0
  if cmds[0] == 'LOGIN':
    cmd = 'SELECT id,email,name,gender,location,last_ip,last_ip_country FROM profiles ORDER BY last_login'
    cmds = cmd.split()
    n = 50
  elif cmds[0] == 'RECENT':
    cmd = 'SELECT id,email,name,gender,location,last_ip,last_ip_country FROM profiles ORDER BY created2'
    cmds = cmd.split()
    n = 50
  elif cmds[0] == 'EMAILS':
    cmd = "SELECT id_from,message FROM (SELECT DISTINCT id_from,message,MAX(sent) FROM emails WHERE message NOT LIKE 'data:image/%%' GROUP BY id_from,message ORDER BY MAX(sent)) sub"
    cmds = cmd.split()
    n = 50
  elif cmds[0].startswith('CONV'):
    cmd = "SELECT * FROM emails WHERE ((id_from=%d AND id_to=%d) OR (id_from=%d AND id_to=%d)) AND message NOT LIKE 'data:image/%%' ORDER BY sent" % (int(cmds[1]), int(cmds[2]), int(cmds[2]), int(cmds[1]))
    cmds = cmd.split()
    n = 20
  try:
    if cmds[0] == 'SELECT':
      db.execute(cmd)
      for entry in db.fetchall()[-n if n else 0:]:
        ss = ', '.join(map(lambda x:unicode(x), entry))
        print ss.encode('utf-8')
    elif cmds[0] == 'DELETE' and cmds[1] == 'MEMBER':
      DeleteMember(int(cmds[2]))
    else:
      db.execute(cmd)
      db.commit()
  except Exception as e:
    print 'Error:', repr(e), 'executing:', cmd

if not sys.stdin.isatty(): # Something available on stdin..
  for line in sys.stdin.readlines():
    command(line)
else:
  while True:
    line = raw_input('SQL: ')
    if line.upper() in ['QUIT', 'EXIT']:
      break
    command(line)
