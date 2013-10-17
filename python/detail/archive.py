#!/usr/bin/env python3

# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

import os
import tarfile
import zipfile

import detail.os
import detail.utility

class Error(Exception):
  pass

class UnknownType(Error):
  pass

class IncorrectFilename(Error):
  """Incorrect filename of an archive
  (raise exception for names like: '.zip', '.rar', ...)

  Need to create extra directory if archive has multiple files inside,
  directory name is archive name without extension, if archive has
  only extension, directory name is empty, bad...

  """
  pass

class AbsoluteFilenames(Error):
  """Files with absolute path inside archive forbidden
  """
  pass

class Type:
  """Type of an archive by file extension.

  self.base - possible output directory (name of archive without extension)
  """
  ZIP = 1
  TAR = 2
  def __init__(self, filename):
    zip_ends = '.zip'
    tar_gz_ends = '.tar.gz'
    if filename.endswith(zip_ends):
      self.type = Type.ZIP
      self.extension = zip_ends
    elif filename.endswith(tar_gz_ends):
      self.type = Type.TAR
      self.extension = tar_gz_ends
    else:
      raise UnknownType(filename)
    length = len(self.extension)
    assert(length != 0)
    self.base = os.path.basename(filename)[0:-length]
    if not self.base:
      raise IncorrectFilename(filename)

class Archive(Type):
  """Wrapper for archives files

  self.separate_directory - output directory of archive
  self.to_path - path that will be printed when unpack (from -> to)
  inherited class must define method (virtual):
    raw_namelist
  """

  def __init__(self, filename):
    self.filename = filename
    Type.__init__(self, filename)
    raw = self.raw_namelist()
    top_file, top_dir =  Archive.check_has_only_one_top(raw)
    if not top_file and not top_dir:
      # some number of files/directories
      # need to create new directory to put them all in one place
      self.separate_directory = self.base
      self.to_path = self.base
    elif top_file and top_dir:
      # same as above, one file and one directory
      self.separate_directory = self.base
      self.to_path = self.base
    elif top_file:
      # only one file to unpack, no directories need
      self.separate_directory = ''
      self.to_path = top_file
    else:
      # output is already only one directory, no need to create new one
      assert(top_dir)
      self.separate_directory = ''
      self.to_path = top_dir

    for x in raw:
      if os.path.isabs(x):
        raise AbsoluteFilenames(
            'arch:{} file:{}'.format(filename, x)
        )

  def namelist(self):
    raw = self.raw_namelist()
    return [os.path.join(self.separate_directory, x) for x in raw]

  def check_has_only_one_top(objects_list):
    """Check that given list of files/directories has one top file or
    one top directory with zero or more files/directories
    """
    # result variables
    top_file = ''
    top_dir = ''
    for x in objects_list:
      dirname, filename = os.path.split(x)
      if dirname:
        dirname = os.path.normpath(dirname)
      if not dirname:
        # filename wants to be top_file
        if top_file:
          # already has one, return no top
          return ('', '')
        top_file = filename
        assert(top_file is not '')
        continue
      if not top_dir:
        top_dir = dirname
        assert(top_dir is not '')
        continue
      if detail.os.first_is_subdirectory_of_second(dirname, top_dir):
        continue
      if detail.os.first_is_subdirectory_of_second(top_dir, dirname):
        top_dir = dirname
        assert(top_dir is not '')
        continue
      return ('', '')
    return (top_file, top_dir)

class ZipArchive(Archive):
  """Wrapper for zipfile.ZipFile class
  """
  def __init__(self, filename):
    self.zipfile = zipfile.ZipFile(filename)
    Archive.__init__(self, filename) # call to raw_namelist
    assert(self.type == Type.ZIP)

  def extractall(self, path):
    self.zipfile.extractall(os.path.join(path, self.separate_directory))

  def raw_namelist(self):
    return self.zipfile.namelist()

class TarArchive(Archive):
  """Wrapper for tarfile.TarFile class
  """
  def __init__(self, filename):
    self.tarfile = tarfile.open(filename)
    Archive.__init__(self, filename) # call to raw_namelist
    assert(self.type == Type.TAR)

  def extractall(self, path):
    self.tarfile.extractall(os.path.join(path, self.separate_directory))

  def raw_namelist(self):
    namelist = []
    for x in self.tarfile.getmembers():
      if x.isdir():
        directory_symbol = os.sep
      else:
        directory_symbol = ''
      namelist.append(x.name + directory_symbol)
    return namelist

def make(filename):
  """Return archive object with methods:
  namelist
  extractall
  """
  type = Type(filename).type
  if type == Type.ZIP:
    return ZipArchive(filename)
  elif type == Type.TAR:
    return TarArchive(filename)
  detail.utility.unreachable()
