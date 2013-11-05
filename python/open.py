#!/usr/bin/env python3

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

# Open files by extension

wiki='https://github.com/ruslo/configs/wiki/open.py-usage'

import argparse
import configparser
import os
import subprocess
import sys

import detail.os_detect
import detail.command

parser = argparse.ArgumentParser(
    description=
        'Open files/directories by extension (config: ~/.open.py).'
        ' See {} for help.'.format(wiki)
)

parser.add_argument(
    'objects',
    nargs='+',
    type=str,
    help='files/directories to open'
)

parser.add_argument(
    '--verbose',
    action='store_true',
    help='print a lot info'
)

args = parser.parse_args()

class Log:
  def __init__(self, verbose):
    self.verbose = verbose

  def p(self, message):
    if not self.verbose:
      return
    print(message)

log = Log(args.verbose)

config_file = '~/.open.py'
config_file = os.path.expanduser(config_file)

conf_parser = configparser.ConfigParser()

if not os.path.exists(config_file):
  sys.exit('File {} not exists'.format(config_file))

conf_parser.read_file(open(config_file))

class Type:
  DIRECTORY = 1
  FILE = 2
  SCRIPT = 3
  NEWFILE = 4

  def name(value):
    if value == Type.DIRECTORY:
      return 'DIRECTORY'
    elif value == Type.FILE:
      return 'FILE'
    elif value == Type.SCRIPT:
      return 'SCRIPT'
    elif value == Type.NEWFILE:
      return 'NEWFILE'
    else:
      sys.exit('Unexpected value')

class Object:
  def __init__(self, filename, openscript):
    self.filename = filename
    self.openscript = openscript
    if os.path.exists(filename):
      self.filename = os.path.abspath(filename)
      if os.path.isdir(filename):
        if detail.os_detect.macosx:
          open_bin = detail.command.get_absolute_path('open')
          if open_bin == '':
            log.p('Warning: "open" not found')
          else:
            self.openscript = open_bin
        self.type = Type.DIRECTORY
      else:
        self.type = Type.FILE
    else:
      # path not exists
      script_path = detail.command.get_absolute_path(filename)
      if script_path == '':
        self.filename = os.path.abspath(filename)
        self.type = Type.NEWFILE
      else:
        log.p('Detected script: {}'.format(script_path))
        self.filename = script_path
        self.type = Type.SCRIPT
    log.p(
        'Add object: filename = {}, open with = {}, type = {}'.format(
            self.filename, self.openscript, Type.name(self.type)
        )
    )

objects = []
for x in args.objects:
  temp, extension = os.path.splitext(x)
  if extension == '':
    openscript = conf_parser['default']['open']
  else:
    try:
      openscript = conf_parser['extensions'][extension]
    except KeyError as exc:
      log.p("Key for '{}' not exists, open with default".format(extension))
      openscript = conf_parser['default']['open']
  objects.append(Object(x, openscript))

all_in_gvim = True
for x in objects:
  if x.openscript != 'gvim.py':
    all_in_gvim = False
    break
  if x.type != Type.FILE:
    all_in_gvim = False
    break

# If all files can be open in gvim, start gvim with tabs
if all_in_gvim:
  cmd = ['gvim.py', '-p']
  for x in objects:
    cmd.append(x.filename)
  log.p('start: {}'.format(cmd))
  subprocess.check_call(cmd)
  sys.exit()

for x in objects:
  cmd = [x.openscript, x.filename]
  log.p('start: {}'.format(cmd))
  subprocess.check_call(cmd)
