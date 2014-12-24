#!/usr/bin/env python3

# Copyright (c) 2014, Ruslan Baratov
# All rights reserved.

import argparse
import os
import stat
import subprocess
import sys

import detail.os
import detail.command

assert(sys.version_info.major == 3)

parser = argparse.ArgumentParser(description='Start windows cmd')
args = parser.parse_args()

explorer_cygpath = detail.command.get_absolute_path('explorer')
explorer_winpath = detail.os.cygwin_to_win(explorer_cygpath)

cwd_winpath = detail.os.cygwin_to_win(os.getcwd())

"""Temporary `.bat` script"""
tmp_path = '/tmp/configs.python.cmd.py-temp.bat'
tmp_winpath = detail.os.cygwin_to_win(tmp_path)

if not os.path.exists(tmp_path):
  temp = open(tmp_path, 'w')
  temp.write('{}:\n'.format(cwd_winpath[0]))
  temp.write('cd "{}"\n'.format(cwd_winpath))
  temp.write('cmd\n')

  os.chmod(
      tmp_path,
      stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR |
      stat.S_IROTH | stat.S_IRGRP | stat.S_IRUSR
  )

subprocess.Popen([
    'cmd',
    '/C',
    'start',
    'clean shell',
    '/I',
    explorer_winpath,
    tmp_winpath
])
