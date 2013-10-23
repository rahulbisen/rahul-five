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
SHARE_HEADER = "SHARE VALUE"
MIN_YEAR = 1990
YEAR_COLUMN = 0
MONTH_COLUMN = 1

class Company():
    """
    class to store per company max share value info
    """
    def __init__(self):
        """
        initialize maxShareList to store only max value info.
        """

        # initialising share valye with a very small negative number.
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
    def __init__(self, csvPath=''):
        """
        initialize row data
        """
        self.csvPath = csvPath

    def processCsvFile(self):
        """
        the main function
        """
        #check if the csv file exists and is readable
        try:
            self.checkCsvPath(self.csvPath)
        except CsvError, e:
            print "Invalid CSV file path:'%s' \n%s"%(self.csvPath, e)
            return
        
        # process CSV file and collect max shares info.
        try:
            self.maxShareDict = self._processCsvFile()
        except CsvError, e:
            print "Invalid data in CSV file:'%s' \n%s"%(self.csvPath, e)
            return
        
        # print self.maxShareDict
        if self.maxShareDict:
            self.displayResults()


    def displayResults(self):

        print "\n\nHighest share value details for companies:"
        print "===========================================\n"

        print "%20s %10s %10s %15s"%(COMPANY_HEADER, YEAR_HEADER, MONTH_HEADER,
                                  SHARE_HEADER)
        for companyName, companyObject in self.maxShareDict.items():
            print "\n"
            for index, shareInfoTuple in enumerate(companyObject.maxShareList):
                if not index:
                    print("%20s %10s %10s %15s"%(companyName, shareInfoTuple[0],
                                                shareInfoTuple[1], shareInfoTuple[2]))
                else:
                    print(" %30s %10s %15s"%(shareInfoTuple[0],
                                                shareInfoTuple[1], shareInfoTuple[2]))

    def _processCsvFile(self):
        #csvFile shoud support iterator protocol hence get a file object.
        csvFile = open(self.csvPath, 'rb')
        csvReader = csv.reader(csvFile, delimiter=',')
        headerList = csvReader.next()

        if not len(headerList) >= 3:
            csvFile.close()
            message = "Insufficient columns in the CSV file. Cannot Process"
            raise CsvError(message)    
            

        # Using ordered dict here to keep track of company name and corresponding
        # max shares data. This is a python 2.7 property.
        maxShareDict = collections.OrderedDict()

        

        """
        companyList = headerList[2:]
        try:
            self.checkUniqueCompanyNames(companyList)
        except CsvError, e:
            raise e
        """

        for companyIndex in range(2, len(headerList)):
            companyName = headerList[companyIndex].strip()
            if companyName in maxShareDict:
                message = "Duplicate entry for Commany Name:%s, column:%s "%(companyName,
                                                                         companyIndex)
                message+= "\nExiting!"
                # close the file
                csvFile.close()
                raise CsvError(message)    
            else:
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

    """
    def checkUniqueCompanyNames(companyList):

        companyNameSet = set(companyList)
        if not len(companyNameSet) == len(companyList):
            raise CsvError("More than one company has the same name. Exiting")

        return True
    """     

    def getIntegerShareValueFromString(self, rowIndex, columnIndex, rowList):
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
        if len(rowList) < len(headerList):
            errorMessage= "Error while processing row:%s. Insufficient share values data." \
                                                              "\n\tIgnoring this row."%rowIndex
            raise CsvError(errorMessage)
        return True


    def checkExtraSharesData(self, rowIndex, rowList, headerList):
        if len(rowList) > len(headerList):
            errorMessage= "Error while processing row:%s. Unexpected extra share value data."\
                                                              "\n\tIgnoring this row."%rowIndex
            raise CsvError(errorMessage)
        return True
        

    def checkCsvPath(self, csvPath):
        """
        check if the csv file exists
        """
        
        try:
            exists = os.path.exists(csvPath)
            if not exists:
                raise Exception("CSV file '%s' does not exist. \nCannot Process" %csvPath)
            if os.path.isdir(csvPath):
                raise Exception("file '%s' is a directory. \nCannot Process." %csvPath)
            if not os.access(csvPath, os.R_OK):
                raise Exception("file '%s' is not readable. \nCannot Process." %csvPath)
        except Exception, e:
            raise CsvError(e.message)

        return True
   
        
#sharesInfo = SharesInfo('C:/Users/rahulbisen/Documents/GitHub/rahul-five/test_data.csv')
#sharesInfo = SharesInfo('test_data.csv')
sharesInfo = SharesInfo('duplicate_test_data.csv')

sharesInfo.processCsvFile()




# if __name__ == '__main__':
#    main()
