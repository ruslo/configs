#!/usr/bin/env python3

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

import argparse
import sys
import tempfile

import detail.argparse
import detail.trash

def main():
  parser = argparse.ArgumentParser(
      description = 'Move files/directories to trash directory'
  )

  parser.add_argument(
      'objects',
      metavar='file-or-dir',
      nargs='+',
      type=detail.argparse.is_dir_or_file,
      help='file or directory to move to trash'
  )

  args = parser.parse_args()

  for objname in args.objects:
    try:
      detail.trash.check_trash_path(objname)
    except detail.trash.TrashDirNotExist as exc:
      sys.exit(exc.message)

  for objname in args.objects:
    detail.trash.trash(objname)

if __name__ == '__main__':
  main()
