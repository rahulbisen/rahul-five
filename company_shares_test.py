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
    """
    Class for testcases for the module SharesInfo
    """
    def setUp(self):
        self.sharesInfo = SharesInfo()
        self.headerList = ['Year', 'Month', 'Company A', 'Company B', 'Company C', 'Company D']
        self.unexpectedYearHeaderList = ['YearS', 'Month', 'Company A', 'Company B']
        self.unexpectedMonthHeaderList = ['Year', 'MonthS', 'Company A', 'Company B']
        self.insufficientHeaderList = ['Year', 'Month']
        self.correctSharesList = ['1990', 'Jan', '2000', '15', '20', '50']
        self.extraSharesList = ['2011', 'Apr', '2000', '200', '20', '70', '90', '120']
        self.missingSharesList = ['2010', 'Mar', '35', '90', '200']
        self.invalidStringSharesList = ['2012', 'May', 'abc', 'def', 'ghi', 'jkh']
        self.invalidYear = '1920'
        self.invalidStringYear = 'not a number'
        self.maxSharesDict = {
                              'Company A' : Company(),
                              'Company B' : Company()
                             }
        self.duplicateCompanyName = self.maxSharesDict.keys()[0]
        self.uniqueCompanyName = 'unique company name'                                    


    ######################################################################
    # tests for SharesInfo.checkCsvPath                                  #
    ######################################################################

    # test SharesInfo.checkCsvPath when no file path is passed.
    def testCheckCsvPathWithNoFilePassed(self):
         
        self.assertRaises(CsvError, self.sharesInfo.checkCsvPath)


    # test SharesInfo.checkCsvPath when None is passed as a file path.
    def testCheckCsvPathWhenFilePassedIsNone(self):
         
        filePath = None
        self.assertRaises(CsvError, self.sharesInfo.checkCsvPath, filePath)


    # test SharesInfo.checkCsvPath when empty string is passed as a file path.
    def testCheckCsvPathWithEmptyStringPassed(self):
         
        filePath = "    "
        self.assertRaises(CsvError, self.sharesInfo.checkCsvPath, filePath)


    # test SharesInfo.checkCsvPath when file path is not a string.
    def testCheckCsvPathWithNonStringPassed(self):
         
        filePath = [10, 20]
        self.assertRaises(CsvError, self.sharesInfo.checkCsvPath, filePath)


    # test SharesInfo.checkCsvPath when file path does not exist.
    def testCheckCsvPathWithNonExistingFile(self):

        filePath = "abcd"
        self.assertRaises(CsvError, self.sharesInfo.checkCsvPath, filePath)


    # test SharesInfo.checkCsvPath when file path is is a directory.
    def testCheckCsvPathWithDirectory(self):

        dirPath = tempfile.mkdtemp(prefix='share_test')
        if  os.path.exists(dirPath):
            self.assertRaises(CsvError, self.sharesInfo.checkCsvPath, dirPath)

            # clear temporary directory
            os.rmdir(dirPath)
        else:
            # this is to cover the case where the dir got deleted for some reason
            message = "Temp directory:%s does not exist. Re-run the test."%dirPath
            self.assertTrue(False, msg=message)


    # test SharesInfo.checkCsvPath when file is not readable by the user.
    # this has to be checked. os.chmod(filePath, 0334) works perfectly on linux
    # making the file unreadable, however it is limited in windows environment
    def testCheckCsvPathWithUnreadableFile(self):

        filePath = tempfile.mkstemp(prefix='share_test')[1]
        if  os.path.exists(filePath):
            os.chmod(filePath, 0334)
            self.assertRaises(CsvError, self.sharesInfo.checkCsvPath, filePath)

            # clear temporary file
            os.chmod(filePath, 0777)
            os.remove(filePath)
        else:
            # this is to cover the case where the dir got deleted for some reason
            message = "Temp file:%s does not exist. Re-run the test."%filePath
            self.assertTrue(False, msg=message)


    # test SharesInfo.checkCsvPath when file path points to a valid file.
    def testCheckCsvPathWithValidFile(self):

        filePath = tempfile.mkstemp(prefix='share_test')[1]
        if  os.path.exists(filePath):
            validFile = self.sharesInfo.checkCsvPath(filePath)
            message = "Valid File: %s"%filePath
            self.assertEqual(validFile, True)

        else:
            # this is to cover the case where the dir got deleted for some reason
            message = "Temp file:%s does not exist. Re-run the test."%filePath
            self.assertTrue(False, msg=message)


    ######################################################################
    # tests for SharesInfo.validateCsvHeaderRow                          #
    ######################################################################

    # test SharesInfo.validateCsvHeaderRow when header data is insufficient
    def testValidateCsvHeaderRowWithInsufficientHeaderFields(self):
        
        self.assertRaises(CsvError, self.sharesInfo.validateCsvHeaderRow,
                                                       self.insufficientHeaderList)


    # test SharesInfo.validateCsvHeaderRow when year in header data does not match
    # 'Year' in Lower, Upper or Mixed case letters.
    def testValidateCsvHeaderRowWithIncorrectYearHeader(self):
        
        self.assertRaises(CsvError, self.sharesInfo.validateCsvHeaderRow,
                                                       self.unexpectedYearHeaderList)


    # test SharesInfo.validateCsvHeaderRow when month in header data does not match
    # 'Month' in Lower, Upper or Mixed case letters.      
    def testValidateCsvHeaderRowWithIncorrectMonthHeader(self):
        
        self.assertRaises(CsvError, self.sharesInfo.validateCsvHeaderRow,
                                                       self.unexpectedMonthHeaderList)
        

    # test SharesInfo.validateCsvHeaderRow when prescribed header data is passed
    def testValidateCsvHeaderRowWithCorrectheaderData(self):

        self.assertTrue(self.sharesInfo.validateCsvHeaderRow(
                                            self.headerList), True)
                                                                
        
    ######################################################################
    # tests for SharesInfo.checkUniqueCompanyNames                       #
    ######################################################################

    # test SharesInfo.checkUniqueCompanyNames with duplicate company names in
    # the header data
    def testCheckUniqueCompanyNamesWithDuplicateCompanyName(self):

        # any column index, based on csv requirements, it will be greater than 2
        # and less than (N+2) where N is the number of companies
        companyIndex = 2
        self.assertRaises(CsvError, self.sharesInfo.checkUniqueCompanyNames, companyIndex,
                          self.duplicateCompanyName, self.maxSharesDict)


    # test SharesInfo.checkUniqueCompanyNames with unique company names in
    # the header data
    def testCheckUniqueCompanyNamesWithUniqueCompanyName(self):

        # any column index, based on csv requirements, it will be greater than 2
        # and less than (N+2) where N is the number of companies
        companyIndex = 2
        self.assertTrue(self.sharesInfo.checkUniqueCompanyNames(companyIndex,
                                self.uniqueCompanyName, self.maxSharesDict), True)
    

    ######################################################################
    # tests for SharesInfo.checkExtraSharesData                          #
    ######################################################################

    # test SharesInfo.checkExtraSharesData with number of elements
    # in the share data more than the number of elements in the Header data.
    def testCheckExtraSharesDataWithExtraShareFields(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertRaises(CsvError, self.sharesInfo.checkExtraSharesData, rowIndex,
                          self.extraSharesList, self.headerList)


    # test SharesInfo.checkExtraSharesData with number of elements
    # in the share data less than the number of elements in the Header data.       
    def testCheckExtraSharesDataWithMissingShareFields(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertTrue(self.sharesInfo.checkExtraSharesData(rowIndex,
                          self.missingSharesList, self.headerList), True)
           

    # test SharesInfo.checkExtraSharesData with number of elements
    # in the share data same as that of the Header data.       
    def testCheckExtraSharesDataWithCorrectShareFields(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertTrue(self.sharesInfo.checkExtraSharesData(rowIndex,
                          self.correctSharesList, self.headerList), True)


    ######################################################################
    # tests for SharesInfo.checkMissingSharesData                        #
    ######################################################################

    # test SharesInfo.checkMissingSharesData with number of elements
    # in the share data more than the number of elements in the Header data.
    def testCheckMissingSharesDataWithMissingShareFields(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertRaises(CsvError, self.sharesInfo.checkMissingSharesData, rowIndex,
                          self.missingSharesList, self.headerList)

        
    # test SharesInfo.checkMissingSharesData with number of elements
    # in the share data more than the number of elements in the Header data.
    def testCheckMissingSharesDataWithExtraShareFields(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertTrue(self.sharesInfo.checkMissingSharesData(rowIndex,
                          self.extraSharesList, self.headerList), True)


    # test SharesInfo.checkMissingSharesData with number of elements
    # in the share data same as that of the Header data.
    def testCheckMissingSharesDataWithCorrectShareFields(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertTrue(self.sharesInfo.checkMissingSharesData(rowIndex,
                          self.correctSharesList, self.headerList), True)


    ######################################################################
    # tests for SharesInfo.verifyYearValue                               #
    ######################################################################

    # test SharesInfo.verifyYearValue with string value that cannot be
    # converted to integer
    def testVerifyYearValueWithInvalidStringYear(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertRaises(CsvError, self.sharesInfo.verifyYearValue, rowIndex,
                          self.invalidStringYear)
        

    # test SharesInfo.verifyYearValue with string value whose integer
    # representation is less that MIN_YEAR ie. 1990
    def testVerifyYearValueWithYearLessThanMinimumYear(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertRaises(CsvError, self.sharesInfo.verifyYearValue, rowIndex,
                          self.invalidYear)
        
    # test SharesInfo.verifyYearValue with `None` passed as the year value.
    def testVerifyYearValueWithYearSetAsNone(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertRaises(CsvError, self.sharesInfo.verifyYearValue, rowIndex,
                          None)
        

    # test SharesInfo.verifyYearValue with valid year string.
    def testVerifyYearValueWithCorrectData(self):

        # any valid row. does not matter
        rowIndex = 3
        self.assertEqual(self.sharesInfo.verifyYearValue(rowIndex,
                          self.correctSharesList[YEAR_COLUMN]), True)


    ######################################################################
    # tests for SharesInfo.getIntegerShareValueFromString                #
    ######################################################################

    # test SharesInfo.getIntegerShareValueFromString with a list of string
    # share values that cannot be converted to their integer representation 
    def testGetIntegerShareValueFromStringWithInvalidStringShares(self):

        # any valid row. does not matter
        rowIndex = 3
        # any column index, based on csv requirements, it will be greater than 2
        # and less than (N+2) where N is the number of companies
        columnIndex = 3
         
        self.assertRaises(CsvError, self.sharesInfo.getIntegerShareValueFromString,
                          rowIndex, columnIndex,
                          self.invalidStringSharesList)

        
    # test SharesInfo.getIntegerShareValueFromString with a list of string
    # share values that can be converted to their integer representation 
    def testGetIntegerShareValueFromStringWithValidData(self):

        # any valid row. does not matter
        rowIndex = 3

        # any column index, based on csv requirements, it will be greater than 2
        # and less than (N+2) where N is the number of companies
        columnIndex = 3

        # self.correctSharesList = ['1990', 'Jan', '2000', '15', '20', '50']
        # so self.correctSharesList[3] should be 15
        shareValue = int(self.correctSharesList[columnIndex].strip())
        
        self.assertEqual(self.sharesInfo.getIntegerShareValueFromString(rowIndex,
                    columnIndex, self.correctSharesList), shareValue)
        

if __name__ == '__main__':
    unittest.main()
