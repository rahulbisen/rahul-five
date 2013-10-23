#!/usr/bin/env python

import sys
import os
import csv
import copy
import unittest
import tempfile

#import classes from company_shares module
from company_shares import Company
from company_shares import SharesInfo
from company_shares import CsvError


class TestCompanyShares(unittest.TestCase):

    def setUp(self):
        pass
    """
    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))
    """

    ######################################################################
    # tests for SharesInfo.checkCsvPath                                  #
    ######################################################################
    
    def testCheckCsvPathWithNonExistingFile(self):
        filePath = "abcd"
        sharesInfo = SharesInfo(filePath)
        self.assertRaises(CsvError, sharesInfo.checkCsvPath, filePath)

    def testCheckCsvPathWithDirectory(self):
        dirPath = tempfile.mkdtemp(prefix='share_test')
        sharesInfo = SharesInfo(dirPath)
        if  os.path.exists(dirPath):
            self.assertRaises(CsvError, sharesInfo.checkCsvPath, dirPath)
        else:
            # this is to cover the case where the dir got deleted for some reason
            message = "Temp directory:%s does not exist. Re-run the test."%dirPath
            self.assertTrue(False, msg=message)

    #this has to be checked. need to fins chmod to disable read
    def testCheckCsvPathWithUnreadableFile(self):
        filePath = tempfile.mkstemp(prefix='share_test')[1]
        sharesInfo = SharesInfo(filePath)
        # filePath = "ll"
        if  os.path.exists(filePath):
            self.assertRaises(CsvError, sharesInfo.checkCsvPath, filePath)
        else:
            # this is to cover the case where the dir got deleted for some reason
            message = "Temp file:%s does not exist. Re-run the test."%filePath
            self.assertTrue(False, msg=message)


    def testCheckCsvPathWithValidRreadableFile(self):
        filePath = tempfile.mkstemp(prefix='share_test')[1]
        sharesInfo = SharesInfo(filePath)
        
        if  os.path.exists(filePath):
            validFile = sharesInfo.checkCsvPath(filePath)
            message = "Valid File: %s"%filePath
            self.assertEqual(validFile, True)
        else:
            # this is to cover the case where the dir got deleted for some reason
            message = "Temp file:%s does not exist. Re-run the test."%filePath
            self.assertTrue(False, msg=message)

    ######################################################################
    # tests for SharesInfo.checkExtraSharesData                          #
    ######################################################################



    """
    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)
    """
if __name__ == '__main__':
    unittest.main()
