#!/usr/bin/env python3

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

import argparse
import os
import sys

import detail.archive
import detail.argparse
import detail.trash
import detail.utility

class Unpacker:
  def parse_argv(self):
    parser = argparse.ArgumentParser(
        description=(
            """Unpack all files to given directory.
            If archive has not one file - directory will be made.
            If there are conflicts between archives - unpack failed
            (example: a.rar -> a.txt, a.zip -> a.txt)
            If archive overwrite files/directories they will be moved to trash
            with trash.py command.
            """
        )
    )
    default_directory = '.' + os.sep
    parser.add_argument(
        '--dir',
        type=detail.argparse.is_dir,
        nargs='?',
        default=default_directory,
        help="destination directory (default is '" + default_directory + "')"
    )
    parser.add_argument(
        'files',
        metavar='file',
        type=argparse.FileType('r'),
        nargs='+',
        help='archive to unpack'
    )
    args = parser.parse_args()
    self.dst_dir = args.dir
    input_file_list = [x.name for x in args.files]
    input_file_list = detail.utility.remove_duplicates(input_file_list)
    try:
      self.arch_list = [detail.archive.make(x) for x in input_file_list]
    except detail.archive.UnknownType as exc:
      sys.exit("Unknown type of file: '{}'".format(str(exc)))

  def check_correct(self):
    self.output_file_list = []
    for x in self.arch_list:
      self.output_file_list += x.namelist()
    without_duplicates = detail.utility.remove_duplicates(self.output_file_list)
    for x in self.output_file_list[:]:
      try:
        without_duplicates.remove(x)
      except ValueError:
        self.report_conflict(x)
    pass

  def report_conflict(self, conflict_file):
    print("conflicting file found: '{}'".format(conflict_file))
    print("in archives:")
    for x in self.arch_list:
      if conflict_file in x.namelist():
        print("  '{}'".format(x.filename))
    sys.exit()

  def trash_conflicting_existent_files(self):
    for x in self.output_file_list:
      if os.path.exists(x):
        detail.trash.trash(x)

  def extractall(self):
    for x in self.arch_list:
      print(
          "extracting: '{}' -> '{}'".format(
              x.filename,
              os.path.join(self.dst_dir, x.to_path)
          )
      )
      x.extractall(self.dst_dir)
    pass

def main():
  unpacker = Unpacker()
  unpacker.parse_argv()
  unpacker.check_correct()
  unpacker.trash_conflicting_existent_files()
  unpacker.extractall()

if __name__ == '__main__':
  main()
