#!/usr/bin/env python

import sys
import os
import csv
import copy

# importing collections to use ordered dictionary in python 2.7
import collections

# CONSTANTS
COMPANY_HEADER = "COMPANY NAME"
YEAR_HEADER = "YEAR"
MONTH_HEADER = "MONTH"
SHARE_HEADER = "MAX SHARE VALUE"
MIN_YEAR = 1990
YEAR_COLUMN = 0
MONTH_COLUMN = 1
YEAR_HEADER = 'YEAR'
MONTH_HEADER = 'MONTH'
MIN_HEADER_COLUMNS = 3


class Company():
    """
    class to store per company max share value info
    """
    def __init__(self):
        """
        initialize maxShareList to store only max value tuples.
        Using list of tuples as companies can maxShareValue for more than one month.
        maxShareList = [(Year, Month, maxShareValue),]
        eg. maxShareList = [('2013', 'Jan', '2000'),]

        :parameters:
            None

        :returns:
            None

        :raises:
            None
            
        """

        # initialising share value with a very small negative number.
        # in normal circumstances, we do not expect the share values
        # to reach this low. This logic could be improved but currently assuming.
   
        # list of tuples for max share info, (year, month, share_value)
        self.maxShareList = [('NA', 'NA', -999999),]


class CsvError(Exception):
    """
    custom exception to raise if CSV file cannot be accessed
    or is not readable or if it contains invalid data.
    """
    #using the default definition of the Exception class
    pass
    

class SharesInfo():
    """
    class to process the CSV file.
    Assuming that the user initialises the class with csv file path
    """
    def __init__(self, csvPath=None):
        """
        Initialize cvsPath with the string passed by the user while
        instantiating the this class.

        :parameters:
            csvPath: `string`
                filepath passed by the user while instantiating the this class.

        :returns:
            None

        :raises:
            None
            
        """
        self.csvPath = csvPath


    def processCsvFile(self):
        """
        This is main function that processes the CSV, parses data and displays results.

        :parameters:
            None

        :returns:
            None

        :raises:
            None
            
        """
        
        #check if the csv file exists and is readable and is not None
        try:
            self.checkCsvPath(self.csvPath)
        except CsvError, e:
            print "Invalid CSV file path:'%s' \n\t%s"%(self.csvPath, e)
            print "Processing Aborted!"
            return
        
        # process CSV file and collect max shares info.
        try:
            self.maxShareDict = self._processCsvFile()
        except CsvError, e:
            print "Invalid data in CSV file:'%s' \n\t%s"%(self.csvPath, e)
            print "Processing Aborted!"
            return
        
        # print self.maxShareDict
        if self.maxShareDict:
            self.displayResults()


    def _processCsvFile(self):
        """
        This is the internal function that processes the CSV and returns a dictionary
        with company name as keys and Company objects as values.
        
        :parameters:
            None

        :returns:
            maxShareDict: `dict`
                dictionary with company name as keys and Company() objects as values.
                maxSharesDict = {
                                  'Company A' : Company(),
                                  'Company B' : Company()
                                }

        :raises:
            Exception: `CsvError`
                if CSV header data is insufficient/invalid
                OR
                if company names in the header data are not unique.
                
            
        """

        #csvFile shoud support iterator protocol hence get a file object.
        csvFile = open(self.csvPath, 'rb')
        csvReader = csv.reader(csvFile, delimiter=',')
        headerList = csvReader.next()

        try:
            self.validateCsvHeaderRow(headerList)
        except CsvError, e:
            csvFile.close()
            raise CsvError(e.message)

        # Using ordered dict here to keep track of company name and corresponding
        # max shares data. This is a python 2.7 property.
        maxShareDict = collections.OrderedDict()

        for companyIndex in range(2, len(headerList)):
            companyName = headerList[companyIndex].strip()

            try:
                self.checkUniqueCompanyNames(companyIndex, companyName, maxShareDict)
            except CsvError, e:
                csvFile.close()
                raise CsvError(e.message)
            
            maxShareDict[companyName] = Company()
       
        rowCount = 0
        for row in csvReader:
            rowCount+= 1
            try:
                self.checkMissingSharesData(rowCount, row, headerList)
                self.checkExtraSharesData(rowCount, row, headerList)
                self.verifyYearValue(rowCount, row[YEAR_COLUMN])
            except CsvError,e:
                print "\n%s \n\tPlease Check the CSV file: %s" %(e, self.csvPath)
                continue
                
            for index, key in enumerate(maxShareDict):
                sharesIndex = index+2
                try:
                    shareValue = self.getIntegerShareValueFromString(rowCount, sharesIndex, row)

                except CsvError, e:
                    print "\n%s \n\tPlease Check the CSV file: %s" %(e, self.csvPath)
                    continue
                
                # companyObject is object of class Company
                companyObject = maxShareDict[key]
                if any(companyObject.maxShareList):
                    newShareInfoTuple = (row[YEAR_COLUMN],row[MONTH_COLUMN], shareValue)
                    for shareInfoTuple in companyObject.maxShareList:
                        if shareValue > shareInfoTuple[2]:
                            companyObject.maxShareList = [newShareInfoTuple]
                            break
                            
                        elif shareValue == shareInfoTuple[2]:
                            companyObject.maxShareList.append(newShareInfoTuple)
                            break
                        
                        else:
                            continue
                else:
                    companyObject.maxShareList.append(newShareInfoTuple) 

        # close the file
        csvFile.close()
                
        return maxShareDict

    
    def displayResults(self):
        """
        Parse the dictionary self.maxShareDict and display results.
        Prints, for each Company years and months in which the share price was highest.
        """
        
        print "\n\nHighest share value details for companies:"
        print "===========================================\n"

        print "%20s %10s %10s %20s"%(COMPANY_HEADER, YEAR_HEADER, MONTH_HEADER,
                                  SHARE_HEADER)
        for companyName, companyObject in self.maxShareDict.items():
            print "\n"
            for index, shareInfoTuple in enumerate(companyObject.maxShareList):
                if not index:
                    print("%20s %10s %10s %20s"%(companyName, shareInfoTuple[0],
                                                shareInfoTuple[1], shareInfoTuple[2]))
                else:
                    print(" %30s %10s %20s"%(shareInfoTuple[0],
                                                shareInfoTuple[1], shareInfoTuple[2]))



    def getIntegerShareValueFromString(self, rowIndex, columnIndex, rowList):
        """
        This function takes in the rowIndex, columnIndex and a shares row info
        in the form of a list of strings and returns the integer value for the
        corresponding string.

        :parameters:
            rowIndex: `int`
                index of the row for logging purpose.

            culumnIndex: `int`
                column index to get a string element from the rowList.

            rowList: `list`
                list of strings representing a row of company shares data.
                
        :returns:
            shareValue: `int`
                integer representation for the string value represented by
                rowIndex and columnIndex.

        :raises:
            Exception: `CsvError`
                if string share value could not be converted to an integer.
            
        """

        try:
            shareValue = int(rowList[columnIndex].strip())

        except ValueError:
            errorMessage = "\nInvalid string value at row:%s,cloumn:%s -> '%s'"%(rowIndex,
                                                 columnIndex, rowList[columnIndex].strip())
            errorMessage+= "\nCould not convert the string into a number."
            raise CsvError(errorMessage)
        
        except Exception, e:
            errorMessage = "Error while processing row:%s,cloumn:%s -> '%s'.\n\t%s"%(rowIndex,
                                                   columnIndex, rowList[columnIndex].strip(),e)
            raise CsvError(errorMessage)
        
        # return integer share value.
        return shareValue


    def verifyYearValue(self, rowIndex, year):
        """
        This function takes in the rowIndex and a string year returns the
        the corresponding integer value.

        :parameters:
            rowIndex: `int`
                index of the row for logging purpose.

            year: `int`
                string value representing an year. eg. '2013'.
               
        :returns:
            `True`: `bool`
                if the function successfully converts the string value to
                an integer.

        :raises:
            Exception: `CsvError`
                if string year value could not be converted to an integer.
                OR
                if the year is older that MIN_YEAR ie. 1990 
            
        """

        try:
            yearValue = int(year.strip())
        except ValueError:
            errorMessage = "\nInvalid string value at row:%s,cloumn:%s -> '%s'"%(rowIndex,
                                                 YEAR_COLUMN, year)
            errorMessage+= "\nCould not convert the string into a number."
            raise CsvError(errorMessage)
        
        except Exception, e:
            errorMessage = "Error while processing row:%s,cloumn:%s -> '%s'.\n\t%s"%(rowIndex,
                                                   YEAR_COLUMN, year,e)
            raise CsvError(errorMessage)

        if yearValue < MIN_YEAR:
            errorMessage = "\nInvalid string value at row:%s,cloumn:%s -> '%s'"%(rowIndex,
                                                 YEAR_COLUMN, year)
            errorMessage+= "\nThe tool only considers data from Year:%s"%MIN_YEAR
            raise CsvError(errorMessage)

        return True    


    def checkMissingSharesData(self, rowIndex, rowList, headerList):
        """
        This function takes in the rowIndex, columnIndex and shares and header list
        info in the form of a list of strings checks if the number of elements in
        the share data are less than the number of elements in the Header data.
        ie. check if some share info is missing

        :parameters:
            rowIndex: `int`
                index of the row for logging purpose.

            culumnIndex: `int`
                index of the column for logging purpose.

            rowList: `list`
                list of strings representing a row of company shares data.

            headerList: `list`
                list of strings representing a row of CSV header data.
                
        :returns:
            `True`: `bool`
                if the element count in rowList is same as that of headerList.
        :raises:
            Exception: `CsvError`
                if the element count in rowList is less than that of headerList.
            
        """

        if len(rowList) < len(headerList):
            errorMessage= "Error while processing row:%s. Insufficient share values data." \
                                                              "\n\tIgnoring this row."%rowIndex
            raise CsvError(errorMessage)
        return True


    def checkExtraSharesData(self, rowIndex, rowList, headerList):
        """
        This function takes in the rowIndex, columnIndex and shares and header list
        info in the form of a list of strings checks if the number of elements in
        the share data are more than the number of elements in the Header data.
        ie. check if unwanted share data exists.

        :parameters:
            rowIndex: `int`
                index of the row for logging purpose.

            culumnIndex: `int`
                index of the column for logging purpose.

            rowList: `list`
                list of strings representing a row of company shares data.

            headerList: `list`
                list of strings representing a row of CSV header data.
                
        :returns:
            `True`: `bool`
                if the element count in rowList is same as that of headerList.
        :raises:
            Exception: `CsvError`
                if the element count in rowList is more than that of headerList.
            
        """

        if len(rowList) > len(headerList):
            errorMessage= "Error while processing row:%s. Unexpected extra share value data."\
                                                              "\n\tIgnoring this row."%rowIndex
            raise CsvError(errorMessage)
        return True


    def checkUniqueCompanyNames(self, companyIndex, companyName, maxShareDict):
        """
        This function checks if a company name already exists as a key in the
        dictionary maxShareDict.

        :parameters:
            companyIndex: `int`
                index of the company column data for logging purpose.

            companyName: `string`
                name of the company in the companyIndex column.

            maxShareDict: `dict`
                dictionary with company name as keys and Company() objects as values.
                eg. maxSharesDict = {
                                     'Company A' : Company(),
                                     'Company B' : Company()
                                    }
                
        :returns:
            `True`: `bool`
                if the companyName is unique.
                ie. companyName does not exist in keys of maxShareDict
                
        :raises:
            Exception: `CsvError`
                if the companyName is not unique.
                if the companyName already exists in maxShareDict.
            
        """

        if companyName in maxShareDict:
            message = "Duplicate entry for Commany Name:%s, column:%s "%(companyName,
                                                                     companyIndex)
            raise CsvError(message)    
        return True
         
        

    def validateCsvHeaderRow(self, headerList):
        """
        Check if the header row is of the below format
        Year,Month,Company A, Company B,Company C, .............Company N
        The row should start with Year,Month and should have atleast
        one company column. Hence MIN_HEADER_COLUMNS = 3 is set as a constant.

        :parameters:
            headerList: `list`
                list of strings representing a row of CSV header data.
                
        :returns:
            `True`: `bool`
                if the header data is valid and has minimum required info in the
                prescribed format.
                
        :raises:
            Exception: `CsvError`
                if no of elements in the headerList are insufficient to comply with
                the prescribed format.
                OR
                if the year(column 1 of CSV file) header does not match 'Year' in
                Lower, Upper or Mixed case letters.
                OR
                if the month(column 2 of CSV file) header does not match 'Year' in
                Lower, Upper or Mixed case letters.
            
        """

        if len(headerList) < MIN_HEADER_COLUMNS:
            message = "Insufficient columns in the CSV file. Probably 'Year'/'Month' or company headers missing"
            raise CsvError(message)    

        if not headerList[YEAR_COLUMN].strip().upper() == YEAR_HEADER:  
            message = "First header column in the CSV file to be 'Year'" \
                      " in Lower, Upper or Mixed case letters. CSV file has '%s'."%headerList[YEAR_COLUMN].strip()
            raise CsvError(message)

        if not headerList[MONTH_COLUMN].strip().upper() == MONTH_HEADER:  
            message = "Second header column in the CSV file to be 'Month'" \
                      " in Lower, Upper or Mixed case letters. CSV file has '%s'."%headerList[MONTH_COLUMN].strip()
            raise CsvError(message)

        return True

    
    def checkCsvPath(self, csvPath=None):
        """
        This function checks if the CSV file is a valid file.
        A file is valid if it exists, is not a directory and is readable.
        
        :parameters:
            csvPath: `string`
                filepath in string format

        :returns:
            `True`: `bool`
                if the csvPath is a valid file.

        :raises:
            Exception: `CsvError`
                if csvPath is not passed or is None.
                OR
                if csvPath is not a string.
                OR
                if the file does not exist.
                OR
                if the file is a directory.
                OR
                if the the file is not readable.
            
        """
        
        try:
            if csvPath is None:
               raise CsvError("Either CSV file is not passed OR is set to None")
            if isinstance(csvPath, str):
                if not csvPath.strip():
                    raise CsvError("CSV file path is an empty string.")
            else:
                raise CsvError("%s is not a valid string." %csvPath)
                               
            exists = os.path.exists(csvPath)
            if not exists:
                raise CsvError("CSV file '%s' does not exist." %csvPath)
            if os.path.isdir(csvPath):
                raise CsvError("file '%s' is a directory." %csvPath)
            if not os.access(csvPath, os.R_OK):
                raise CsvError("file '%s' is not readable." %csvPath)
        except Exception, e:
            raise CsvError(e.message)

        return True
   
        
#sharesInfo = SharesInfo('C:/Users/rahulbisen/Documents/GitHub/rahul-five/test_data.csv')
#sharesInfo = SharesInfo('test_data.csv')
#sharesInfo = SharesInfo('duplicate_company_test_data.csv')
#sharesInfo = SharesInfo('invalid_header_test_data.csv')
#sharesInfo = SharesInfo("   ")
#sharesInfo = SharesInfo(None)
#sharesInfo = SharesInfo()
#sharesInfo.processCsvFile()




# if __name__ == '__main__':
#    main()
