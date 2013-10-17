#!/usr/bin/env python3

import sys
sys.path.append('../..')

import unittest
import os

test_dir_path = 'archive/zip'

class TypeTest(unittest.TestCase):
  def test_simple_correct(self):
    from detail.archive import Type
    x = Type('abc.zip')
    self.assertEqual(x.type, Type.ZIP)
    self.assertEqual(x.base, 'abc')

  def test_with_directories_correct(self):
    from detail.archive import Type
    x = Type('a/b/c/abc.zip')
    self.assertEqual(x.type, Type.ZIP)
    self.assertEqual(x.base, 'abc')

  def test_raise_if_unknown(self):
    import detail.archive
    from detail.archive import Type
    self.assertRaises(detail.archive.UnknownType, Type, ('abc.zipa'))
    self.assertRaises(detail.archive.IncorrectFilename, Type, ('.zip'))
    self.assertRaises(detail.archive.IncorrectFilename, Type, ('a/b/c/.zip'))

class ArchiveTest(unittest.TestCase):
  def test_one_top(self):
    from detail.archive import Archive
    self.assertEqual(Archive.check_has_only_one_top(['a.txt']), ('a.txt', ''))
    self.assertEqual(
        Archive.check_has_only_one_top(['a/', 'a/b.txt']),
        ('', 'a')
    )
    self.assertEqual(
        Archive.check_has_only_one_top(['./a/', 'a/']),
        ('', 'a')
    )
    self.assertEqual(
        Archive.check_has_only_one_top(['a/', 'a/b.txt', 'a/x.txt']),
        ('', 'a')
    )
    self.assertEqual(
        Archive.check_has_only_one_top(['a/x.txt', 'a/b.txt', 'a/']),
        ('', 'a')
    )
    self.assertEqual(
        Archive.check_has_only_one_top([
            'dir/',
            'dir/a.txt',
            'dir/b.txt',
            'dir/c.txt',
            'dir/d.txt',
            'dir/e.txt'
        ]),
        ('', 'dir')
    )
    self.assertEqual(
        Archive.check_has_only_one_top(['a/', 'b/']),
        ('', '')
    )
    self.assertEqual(
        Archive.check_has_only_one_top(['a.txt', 'b.txt']),
        ('', '')
    )
    self.assertEqual(
        Archive.check_has_only_one_top(['a/', 'b.txt']),
        ('b.txt', 'a')
    )
    self.assertEqual(
        Archive.check_has_only_one_top(['a/', 'abc/b.txt']),
        ('', '')
    )
    self.assertEqual(
        Archive.check_has_only_one_top(['a/', 'b/b.txt', 'a/x.txt']),
        ('', '')
    )

class ZipArchiveTest(unittest.TestCase):
  def setUp(self):
    from detail.shutil import rmtree
    self.temp_path = './__tmp_testing__'
    rmtree(self.temp_path)
    os.mkdir(self.temp_path)
    self.assertEqual(
        [x for x in os.walk(self.temp_path)],
        [('./__tmp_testing__', [], [])]
    )

  def tearDown(self):
    from detail.shutil import rmtree
    self.temp_path = './__tmp_testing__'
    rmtree(self.temp_path)

  def test_one_file_one_archive(self):
    from detail.archive import ZipArchive
    arch = ZipArchive(
        os.path.join(test_dir_path, 'one file - one archive.zip')
    )
    self.assertEqual(arch.namelist(), ['a.txt'])
    arch.extractall(self.temp_path)
    self.assertEqual(
        [x for x in os.walk(self.temp_path)],
        [('./__tmp_testing__', [], ['a.txt'])]
    )

  def test_one_directory_with_files(self):
    from detail.archive import ZipArchive
    from detail.archive import Archive
    arch = ZipArchive(
        os.path.join(test_dir_path, 'one directory with files.zip')
    )
    top_file, top_dir = Archive.check_has_only_one_top(arch.raw_namelist())
    self.assertEqual(top_file, '')
    self.assertEqual(top_dir, 'dir', arch.raw_namelist())
    self.assertEqual(arch.separate_directory, '')
    self.assertEqual(
        arch.namelist(),
        [
            'dir/',
            'dir/a.txt',
            'dir/b.txt',
            'dir/c.txt',
            'dir/d.txt',
            'dir/e.txt'
        ]
    )
    arch.extractall(self.temp_path)
    self.assertEqual(
        [x for x in os.walk(self.temp_path)],
        [
            ('./__tmp_testing__', ['dir'], []),
            (
                './__tmp_testing__/dir',
                [],
                ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt']
            )
        ]
    )

  def test_directory_tree(self):
    from detail.archive import ZipArchive
    """archive consist of two directories, check new prefix directory added"""
    arch = ZipArchive(
        os.path.join(test_dir_path, 'directory tree.zip')
    )
    self.assertEqual(
        arch.namelist(),
        [
            'directory tree/dir1/',
            'directory tree/dir1/a.txt',
            'directory tree/dir1/b.txt',
            'directory tree/dir1/c.txt',
            'directory tree/dir1/d.txt',
            'directory tree/dir1/e.txt',
            'directory tree/dir2/',
            'directory tree/dir2/a.txt',
            'directory tree/dir2/b.txt',
            'directory tree/dir2/c.txt',
            'directory tree/dir2/d.txt',
            'directory tree/dir2/e.txt'
        ]
    )
    arch.extractall(self.temp_path)
    self.assertEqual(
        [x for x in os.walk(self.temp_path)],
        [
            ('./__tmp_testing__', ['directory tree'], []),
            ('./__tmp_testing__/directory tree', ['dir1', 'dir2'], []),
            (
                './__tmp_testing__/directory tree/dir1',
                [],
                ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt']
            ),
            (
                './__tmp_testing__/directory tree/dir2',
                [],
                ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt']
            )
        ]
    )

  def test_directory_multiple_files_one_archive(self):
    from detail.archive import ZipArchive
    arch = ZipArchive(
        os.path.join(test_dir_path, 'multiple files - one archive.zip')
    )
    self.assertEqual(
        arch.namelist(),
        [
            'multiple files - one archive/a.txt',
            'multiple files - one archive/b.txt',
            'multiple files - one archive/c.txt',
            'multiple files - one archive/d.txt',
            'multiple files - one archive/e.txt',
        ]
    )
    arch.extractall(self.temp_path)
    self.assertEqual(
        [x for x in os.walk(self.temp_path)],
        [
            ('./__tmp_testing__', ['multiple files - one archive'], []),
            (
                './__tmp_testing__/multiple files - one archive',
                [],
                ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt']
            )
        ]
    )

  def test_multiple_files_multiple_parts_of_archive(self):
    # TODO, python not support multiple-disk zip
    pass

  def test_one_file_multiple_parts_of_archive(self):
    # TODO, python not support multiple-disk zip
    pass

class MakeTest(unittest.TestCase):
  def test_creation(self):
    import os
    import detail.archive
    from detail.archive import make
    from detail.archive import Type
    test_file_path = os.path.join(test_dir_path, 'one file - one archive.zip')
    self.assertEqual(make(test_file_path).type, Type.ZIP)
    self.assertRaises(detail.archive.UnknownType, make, ('abc.zipa'))
    self.assertRaises(detail.archive.UnknownType, make, ('zip'))
    self.assertRaises(detail.archive.UnknownType, make, ('a.qzip'))

if __name__ == '__main__':
  unittest.main()
