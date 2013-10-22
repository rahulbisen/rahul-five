#!/usr/bin/env python

import sys
import os
import csv
import collections

# comment
class Company():
    """
    class to store per company data
    """
    def __init__(self):
        """
        initialize variable to store only Maxed info.
        """
        self.maxYear = "NA"
        self.maxMonth = "NA"
        # initialising with a very small negative number
        # in normal circumstances, we do not expect the share values
        # to reach this low. This could be improved but currently assuming.
        
        self.maxShareValue = -999999
        

class CsvError(Exception):
    """
    custom exception to raise if CSV file cannot be accessed
    or is not readable.
    """
    #using the default definition of the Exception class
    pass
    

class SharesInfo():
    """
    class to process the CSV file.
    Assuming that the user initialises the class with csv file path
    """
    def __init__(self, csvPath):
        """
        initialize row data
        """
        self.csvPath = csvPath

    def main(self):
        """
        the main function
        """
        #check if the csv file exists and is readable
        try:
            self.checkCsvPath(self.csvPath)
        except CsvError, e:
            print "Invalid CSV file path:%s \n%s"%(self.csvPath, e)
            return
        
        # process CSV file and collect max shares info.
        try:
            self.maxShareDict = self.processCsvFile()
        except CsvError, e:
            print "Invalid data in CSV file:%s \n%s"%(self.csvPath, e)
            return
        # print self.maxShareDict
        self.displayResults()

    def displayResults(self):
        print "\n\n"
        for companyName, companyObject in self.maxShareDict.items():
            print companyName
            print "*****************"
            print "year:", companyObject.maxYear
            print "month:", companyObject.maxMonth
            print "maxShareValue:", companyObject.maxShareValue
            print "\n\n"
            
    def processCsvFile(self):
        #csvFile shoud support iterator protocol hence get a file object.
        csvFile = open(self.csvPath, 'rb')
        csvReader = csv.reader(csvFile, delimiter=',')
        headerList = csvReader.next()

        """
        companysCount = len(headerList)-2


        # initialise sharesCacheList with dummy year and month
        sharesCacheList = ['1990', 'Jan']
        # and share value of 0 for N companies
        for i in range(companysCount):
            sharesCacheList.append(0)
        """    
        # Using ordered dict here to keep track of company name and corresponding
        # max shares data. This is a python 2.7 property.
        maxShareDict = collections.OrderedDict()
        
        for companyIndex in range(2, len(headerList)):
            companyName = headerList[companyIndex].strip()
            if companyName in maxShareDict:
                print "duplicate entry for Conmany Name:%s, column:%s "%(companyName,
                                                                         companyIndex)
                raise CsvError("More than one company shares the same name. Exiting")    
            else:
                maxShareDict[companyName] = Company()

       
        rowCount = 0
        for row in csvReader:
            rowCount+= 1
            if len(row) < len(headerList):
                print "row %s has missing data. Not considering this row"%rowCount
                print "Please check the CSV file: %s" %self.csvPath
                continue
            elif len(row) > len(headerList):
                print "row %s has extra data. Not considering this row"%rowCount
                print "Please check the CSV file: %s" %self.csvPath
                continue
            else:
                pass


            """        
            for index in range(2,len(headerList)):
                try:
                    shareValue = int(row[i].strip())
                except Exception,e:
                    print "Invalid value on row:%s, cloumn:%s \n%s"%(rowCount, sharesIndex, e)
                    continue
                if shareValue > sharesCacheList[i]:
            """     

            for index, key in enumerate(maxShareDict):
                sharesIndex = index+2
                try:
                    shareValue = int(row[sharesIndex].strip())
                except Exception,e:
                    print "Invalid value on row:%s, cloumn:%s \n%s"%(rowCount, sharesIndex, e)
                    # maxShareDict[key].maxShareValue = 'NA'
                    continue
                
                # companyObject is object of class Company
                companyObject = maxShareDict[key]
                if shareValue > companyObject.maxShareValue:
                    companyObject.maxShareValue = shareValue
                    companyObject.maxYear = row[0]
                    companyObject.maxMonth = row[1]

        return maxShareDict
        
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

   
        
sharesInfo = SharesInfo('C:/Users/rahulbisen/Documents/GitHub/rahul-five/test_data.csv')
sharesInfo.main()
