#!/usr/bin/env python3

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

# This is a wrapper/switcher to gvim/vim editor

import os
import subprocess
import sys

import detail.os_detect
import detail.command

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

def vim_binary():
  if detail.os_detect.macosx:
    return vim_macosx_binary()
  else:
    return 'gvim'

vim_argv[0] = vim_binary()

if detail.command.test_exists(vim_argv[0]):
  if detail.os_detect.macosx:
    vim_argv.insert(1, '-g')
else:
  # gvim not found, downgrade to vim
  vim_argv[0] = 'vim'
  detail.check_exists(vim_argv[0])

log.p('call: {}'.format(vim_argv))

# do not call |command.run| (tested with '-f' option)
try:
  subprocess.check_call(vim_argv)
except subprocess.CalledProcessError:
  sys.exit('Call to (g)vim failed')
