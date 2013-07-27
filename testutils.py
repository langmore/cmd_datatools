import unittest
from StringIO import StringIO
import sys
from numpy.testing import assert_allclose
from datetime import datetime

import common, subsample, cut
"""
To run, from the test/ directory, type:
$ python -m unittest test_utils

OR for verbose output
$ python -m unittest -v test_utils

OR to run only the methods in TestCut
$ python -m unittest test_utils.TestCut

OR to run only the TestCut.test_cut_file_keepname method
$ python -m unittest test_utils.TestCut.test_cut_file_keepname
"""


class TestCut(unittest.TestCase):
    """
    Tests the implementation (but not the interface) of cut.py
    """
    def setUp(self):
        self.outfile = StringIO()

        commastring = \
        "name,age,weight\r\nian,1,11\r\ndaniel,2,22\r\nchang,3,33"
        self.commafile = StringIO(commastring)

        pipestring = \
        "name|age|weight\r\nian|1|11\r\ndaniel|2|22\r\nchang|3|33"
        self.pipefile = StringIO(pipestring)

    def test_cut_file_keepname(self):
        cut.cut_file(self.commafile, self.outfile, keep_list=['name'])
        result = self.outfile.getvalue()
        self.assertEqual('name\r\nian\r\ndaniel\r\nchang\r\n', result)

    def test_cut_file_keepnameage(self):
        cut.cut_file(self.commafile, self.outfile, keep_list=['name', 'age'])
        result = self.outfile.getvalue()
        self.assertEqual('name,age\r\nian,1\r\ndaniel,2\r\nchang,3\r\n', result)

    def test_cut_file_keepagename(self):
        cut.cut_file(self.commafile, self.outfile, keep_list=['age', 'name'])
        result = self.outfile.getvalue()
        self.assertEqual('age,name\r\n1,ian\r\n2,daniel\r\n3,chang\r\n', result)

    def test_cut_file_keepagename_pipe(self):
        cut.cut_file(
            self.pipefile, self.outfile, keep_list=['age', 'name'],
            delimiter='|')
        result = self.outfile.getvalue()
        self.assertEqual('age|name\r\n1|ian\r\n2|daniel\r\n3|chang\r\n', result)

    def test_cut_file_keepempty(self):
        """
        Test keeping no columns
        """
        cut.cut_file(self.commafile, self.outfile, keep_list=[])
        result = self.outfile.getvalue()
        self.assertEqual('\r\n\r\n\r\n\r\n', result)

    def test_cut_file_keepNone(self):
        """
        Test keeping no columns
        """
        cut.cut_file(self.commafile, self.outfile, keep_list=None)
        result = self.outfile.getvalue()
        self.assertEqual('\r\n\r\n\r\n\r\n', result)

    def tearDown(self):
        self.outfile.close()


class TestSubsample(unittest.TestCase):
    """
    Tests the subsampler
    """
    def setUp(self):
        self.outfile = StringIO()
        self.commafile = StringIO(
            'name,age,weight\nian,1,11\ndaniel,2,22\nchang,3,33')
        self.pipefile = StringIO(
            'name|age|weight\nian|1|11\ndaniel|2|22\nchang|3|33')
        self.longfile = StringIO(
            'name,age,weight\nian,1,11\ndaniel,2,22\nian,1b,11b\nchang,3,33'
            '\ndaniel,2b,22b\nchang,3b,33b')
        self.seed = 1234

    def test_r0p0_comma(self):
        subsample.subsample(
            self.commafile, self.outfile, subsample_rate=0.0, seed=self.seed)
        result = self.outfile.getvalue()
        benchmark = 'name,age,weight\r\n'
        self.assertEqual(result, benchmark)

    def test_r0p5_comma(self):
        subsample.subsample(
            self.commafile, self.outfile, subsample_rate=0.5, seed=self.seed)
        result = self.outfile.getvalue()
        benchmark = 'name,age,weight\r\nian,1,11\r\nchang,3,33\r\n'
        self.assertEqual(result, benchmark)

    def test_r0p5_pipe(self):
        subsample.subsample(
            self.pipefile, self.outfile, subsample_rate=0.5, seed=self.seed)
        result = self.outfile.getvalue()
        benchmark = 'name|age|weight\r\nian|1|11\r\nchang|3|33\r\n'
        self.assertEqual(result, benchmark)

    def test_r0p5_keyname_comma(self):
        subsample.subsample(
            self.longfile, self.outfile, subsample_rate=0.5,
            key_column='name', seed=self.seed)
        result = self.outfile.getvalue()
        benchmark = 'name,age,weight\r\nian,1,11\r\nian,1b,11b\r\nchang,3,33'\
            '\r\nchang,3b,33b\r\n'
        self.assertEqual(result, benchmark)

    def tearDown(self):
        self.outfile.close()
