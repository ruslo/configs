#!/usr/bin/env python3

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

import os

# remove when move to 3.3
def rmtree(path):
  for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
      os.remove(os.path.join(dirpath, filename))
    for dirname in dirnames:
      rmtree(os.path.join(dirpath, dirname))
    os.rmdir(dirpath)
