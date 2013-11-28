#!/usr/bin/env python3

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

# This is a wrapper/switcher to gvim/vim editor

wiki='https://github.com/ruslo/configs/wiki/gvim.py-usage'

import os
import subprocess
import sys

import detail.command
import detail.os
import detail.os_detect

vim_argv = sys.argv

class Log:
  def __init__(self, verbose):
    self.verbose = verbose

  def p(self, message):
    if not self.verbose:
      return
    print(message)

print_verbose = '--verbose' in vim_argv
log = Log(print_verbose)
if print_verbose:
  vim_argv.remove('--verbose')

def mac_vim_app_directory():
  """Try to detect MacVim.app location"""
  vim_app_dir = os.getenv('VIM_APP_DIR')
  if vim_app_dir:
    log.p('VIM_APP_DIR detected')
    macvim_app_dir = os.path.join(vim_app_dir, 'MacVim.app')
    if os.path.exists(macvim_app_dir):
      return macvim_app_dir
    sys.exit("Error: VIM_APP_DIR variable don't point to MacVim.app directory")
  search_paths = [
      '~/Applications',
      '~/Applications/vim',
      '/Applications',
      '/Applications/vim',
      '/Applications/Utilities',
      '/Applications/Utilities/vim'
  ]
  for location in search_paths:
    macvim_app_dir = os.path.join(location, 'MacVim.app')
    macvim_app_dir = os.path.expanduser(macvim_app_dir)
    log.p('test location: {}'.format(macvim_app_dir))
    if os.path.exists(macvim_app_dir):
      return macvim_app_dir
  print("Used environment variable: VIM_APP_DIR")
  print("Used standard paths: {}".format(search_paths))
  sys.exit("Error: can't find MacVim.app directory")

def vim_macosx_binary():
  """Try to detect MacVim.app directory with Vim binary"""
  dir = mac_vim_app_directory()
  bin = os.path.join(dir, 'Contents', 'MacOS', 'Vim')
  if os.path.exists(bin):
    return bin
  sys.exit("Error: path '{}' not exists".format(bin))

def vim_cygwin_binary():
  """Try to detect gvim.exe in %ProgramFiles???%/Vim"""
  progfiles = os.getenv('PROGRAMFILES')
  if not progfiles:
    sys.exit("Can't detect PROGRAMFILES (see {} for help)".format(wiki))
  progfiles = detail.os.win_to_cygwin(progfiles)
  progfiles = os.path.join(progfiles, 'Vim')
  for root, dirs, files in os.walk(progfiles):
    if 'gvim.exe' in files:
      return os.path.join(root, 'gvim.exe')
  sys.exit("gvim.exe not found (see {} for help)".format(wiki))

def vim_binary():
  if detail.os_detect.macosx:
    return vim_macosx_binary()
  elif detail.os_detect.cygwin:
    return vim_cygwin_binary()
  else:
    return 'gvim'

vim_argv[0] = vim_binary()

if detail.command.test_exist(vim_argv[0]):
  if detail.os_detect.macosx:
    vim_argv.insert(1, '-g')
else:
  # gvim not found, downgrade to vim
  vim_argv[0] = 'vim'
  detail.command.check_exist(vim_argv[0])

if detail.os_detect.cygwin:
  for index, entry in enumerate(vim_argv):
    """substitute all files cygwin path to windows path"""
    if index == 0:
      continue
    if entry.startswith('-'):
      continue
    vim_argv[index] = detail.os.cygwin_to_win(entry)
  # Add shell variable update (for diff mode)
  cmd = detail.command.run(['which', 'cmd'])
  assert(len(cmd) == 1)
  cmd = cmd[0]
  vim_argv.append('--cmd')
  vim_argv.append('set shell={}'.format(detail.os.cygwin_to_win(cmd)))

log.p('call: {}'.format(vim_argv))

try:
  if detail.os_detect.cygwin and not '-f' in vim_argv:
    new_vim_argv = []
    for x in vim_argv:
      new_vim_argv.append("'{}'".format(x))
    os.system(' '.join(new_vim_argv) + ' &')
  else:
    # do not call |command.run| (tested with '-f' option)
    subprocess.check_call(vim_argv)
except subprocess.CalledProcessError:
  sys.exit('Call to (g)vim failed')
