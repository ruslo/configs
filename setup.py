#!/usr/bin/env python3

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

import argparse
import difflib
import os
import platform
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(
    description = """
        Setup config files. Copy files to it's HOME locations.
        If file (or directory) not exist, it will be created.
        If destination file is equal to source file plus some additional info
        (extended version), this file will be skipped. Otherwise if files not
        equal - command |gvim.py -d| will be started to show/resolve diffs.
    """
)

parser.add_argument(
    '--gitenv-root',
    dest='gitenv',
    nargs='?',
    default='',
    help="GITENV_ROOT directory (will be added to .bashrc file)"
)

parser.add_argument(
    '--force',
    action='store_true',
    help='overwrite all existing files'
)

args = parser.parse_args()

configs_dir = os.path.dirname(os.path.abspath(__file__))
bashrc_abs_path = os.path.join(configs_dir, 'unix', 'bashrc')
zshrc_abs_path = os.path.join(configs_dir, 'unix', 'zshrc')
if not os.path.exists(bashrc_abs_path):
  sys.exit("file '{}' not exists".format(bashrc_abs_path))

# generate .bashrc base file
bashrc_base_abs = bashrc_abs_path + '.temp'
bashrc_base = open(bashrc_base_abs, mode='w')
gitenv_root = args.gitenv
if gitenv_root:
  bashrc_base.write('export GITENV_ROOT="{}"\n'.format(gitenv_root))
  bashrc_base.write('source "${GITENV_ROOT}/configs/unix/bashrc"\n')
  bashrc_path = os.path.join(gitenv_root, 'configs', 'unix', 'bashrc')
  if not os.path.exists(bashrc_path):
    sys.exit("file '{}' not exists".format(bashrc_path))
else:
  bashrc_base.write('source "{}"\n'.format(bashrc_abs_path))
bashrc_base.close()

# generate .zshrc base file
zshrc_base_abs = zshrc_abs_path + '.temp'
zshrc_base = open(zshrc_base_abs, mode='w')
if gitenv_root:
  zshrc_base.write('export GITENV_ROOT="{}"\n'.format(gitenv_root))
  zshrc_base.write('source "${GITENV_ROOT}/configs/unix/zshrc"\n')
  zshrc_path = os.path.join(gitenv_root, 'configs', 'unix', 'zshrc')
  if not os.path.exists(zshrc_path):
    sys.exit("file '{}' not exists".format(zshrc_path))
else:
  zshrc_base.write('source "{}"\n'.format(zshrc_abs_path))
zshrc_base.close()

if platform.system().startswith('CYGWIN'):
  home = os.getenv('HOME')
  bash_profile_dst = os.path.join(home, '.bash_profile')
  bash_profile_src = os.path.join(configs_dir, 'unix', 'bash_profile')
  if not os.path.exists(bash_profile_dst):
    shutil.copyfile(bash_profile_src, bash_profile_dst)

# emulate enum
class Result:
  equal = 0
  bigger = 1
  not_bigger = 2

def second_text_file_is_bigger(file_1, file_2):
  file_1_id = open(file_1)
  file_2_id = open(file_2)
  diff_list = difflib.Differ().compare(
      file_1_id.readlines(),
      file_2_id.readlines()
  )
  bigger = False
  for x in diff_list:
    if x.startswith('- '):
      return Result.not_bigger
    elif x.startswith('+ '):
      bigger = True
    elif x.startswith('? '):
      pass
    else:
      assert(x.startswith('  '))
      pass
  if bigger:
    return Result.bigger
  else:
    return Result.equal

def run_setup(src, dst):
  dst = os.path.expanduser(dst)
  src = os.path.join(configs_dir, src)
  dst_dir = os.path.dirname(dst)
  if not os.path.exists(dst_dir):
    os.makedirs(dst_dir, exist_ok = True)
  if os.path.exists(dst) and args.force:
    os.remove(dst)
  if not os.path.exists(dst):
    if os.path.lexists(dst):
      sys.exit("'{}' is broken link, please remove it".format(dst))
    print("Init: {} -> {}".format(src, dst))
    shutil.copyfile(src, dst)
    return
  result = second_text_file_is_bigger(src, dst)
  if result == Result.equal:
    print("{} not changed".format(dst))
    return
  if result == Result.bigger:
    print(
        "File '{}' is equal to '{}' + some"
        " new content (skip)".format(dst, src)
    )
    return
  assert(result == Result.not_bigger)
  gvim_path = os.path.join(configs_dir, 'python', 'gvim.py')
  print("Run diff: '{}' vs. '{}'".format(src, dst))
  # do not use check_output; vim version need to be shown
  subprocess.check_call([gvim_path, '-d', src, dst])

run_setup('python/config.open.py', '~/.open.py')
run_setup('unix/bashrc.temp', '~/.bashrc')
run_setup('unix/zshrc.temp', '~/.zshrc')
run_setup('unix/bash_profile', '~/.bash_profile')
run_setup('vim/c.vim', '~/.vim/after/syntax/c.vim')
run_setup('vim/rst.vim', '~/.vim/after/syntax/rst.vim')
run_setup('vim/gitcommit.vim', '~/.vim/after/syntax/gitcommit.vim')
run_setup('vim/vimrc', '~/.vimrc')
run_setup('vim/vimrc', '~/_vimrc')
run_setup('vim/vimrc', '~/_vsvimrc')
run_setup('git/config', '~/.gitconfig')
run_setup('git/attributes', '~/.config/git/attributes')
