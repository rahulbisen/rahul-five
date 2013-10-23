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
from company_shares import MIN_YEAR
from company_shares import YEAR_COLUMN
from company_shares import MONTH_COLUMN

class TestCompanyShares(unittest.TestCase):

    def setUp(self):
        self.headerList = ['Year','Month','Company A', 'Company B', 'Company C', 'Company D']
        self.correctSharesList = ['1990', 'Jan', '2000', '15', '20', '50']
        self.extraSharesList = ['2011', 'Apr', '2000', '200', '20', '70', '90', '120']
        self.missingSharesList = ['2010', 'Mar', '35', '90', '200']
        self.invalidYear = '1920'
        self.invalidStringYear = 'not a number'
        self.invalidStringSharesList = ['2012', 'May', 'abc', 'def', 'ghi', 'jkh']

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

    def testCheckExtraSharesDataWithExtraShareFields(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertRaises(CsvError, sharesInfo.checkExtraSharesData, rowIndex,
                          self.extraSharesList, self.headerList)
        
    def testCheckExtraSharesDataWithMissingShareFields(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertTrue(sharesInfo.checkExtraSharesData(rowIndex,
                          self.missingSharesList, self.headerList), True)
           

    def testCheckExtraSharesDataWithCorrectShareFields(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertTrue(sharesInfo.checkExtraSharesData(rowIndex,
                          self.correctSharesList, self.headerList), True)


    ######################################################################
    # tests for SharesInfo.checkMissingSharesData                        #
    ######################################################################

    def testCheckMissingSharesDataWithMissingShareFields(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertRaises(CsvError, sharesInfo.checkMissingSharesData, rowIndex,
                          self.missingSharesList, self.headerList)
        

    def testCheckMissingSharesDataWithExtraShareFields(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertTrue(sharesInfo.checkMissingSharesData(rowIndex,
                          self.extraSharesList, self.headerList), True)


    def testCheckMissingSharesDataWithCorrectShareFields(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertTrue(sharesInfo.checkMissingSharesData(rowIndex,
                          self.correctSharesList, self.headerList), True)


    ######################################################################
    # tests for SharesInfo.verifyYearValue                               #
    ######################################################################

    def testVerifyYearValueWithInvalidStringYear(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertRaises(CsvError, sharesInfo.verifyYearValue, rowIndex,
                          self.invalidStringYear)
        

    def testVerifyYearValueWithYearLessThanMinimumYear(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertRaises(CsvError, sharesInfo.verifyYearValue, rowIndex,
                          self.invalidYear)
        

    def testVerifyYearValueWithYearSetAsNone(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertRaises(CsvError, sharesInfo.verifyYearValue, rowIndex,
                          None)
        

    def testVerifyYearValueWithCorrectData(self):
        # any valid row. does not matter
        rowIndex = 3
        sharesInfo = SharesInfo()
        self.assertEqual(sharesInfo.verifyYearValue(rowIndex,
                          self.correctSharesList[YEAR_COLUMN]), True)

    ######################################################################
    # tests for SharesInfo.getIntegerShareValueFromString                #
    ######################################################################

    def testGetIntegerShareValueFromStringWithInvalidStringShares(self):
        # any valid row. does not matter
        rowIndex = 3
        # any column index, based on csv requirements, it will be greater than 2
        # and less than (N+2) where N is the number of companies
        columnIndex = 3
        sharesInfo = SharesInfo()
        self.assertRaises(CsvError, sharesInfo.getIntegerShareValueFromString,
                          rowIndex, columnIndex,
                          self.invalidStringSharesList)
        

    def testGetIntegerShareValueFromStringWithValidData(self):
        # any valid row. does not matter
        rowIndex = 3
        # any column index, based on csv requirements, it will be greater than 2
        # and less than (N+2) where N is the number of companies
        columnIndex = 3

        # self.correctSharesList = ['1990', 'Jan', '2000', '15', '20', '50']
        # so self.correctSharesList[3] should be 15
        shareValue = int(self.correctSharesList[columnIndex].strip())
        
        sharesInfo = SharesInfo()
        self.assertEqual(sharesInfo.getIntegerShareValueFromString(rowIndex,
                    columnIndex, self.correctSharesList), shareValue)
        


    """
    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)
    """
if __name__ == '__main__':
    unittest.main()
