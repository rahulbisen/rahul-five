#!/usr/bin/env python

import sys
import os
import csv
import copy

#import SharesInfo from company_shares module
from company_shares import SharesInfo

# constants
TEST_CSV_PATH = './test_data.csv'

def main():
    """
    Call SharesInfo methods to process the CSV
    """
    displayMainMenu()
                  
def displayMainMenu():

    print "\n\nOptions Menu:"
    print "*****************"
    print "1. Enter the CSV file path to process:"
    print "2. Test using the test CSV file in the tool dir."
    print "3. Exit"
    
    while(True):
        choice = raw_input('Enter the choice(1-3): ')
        try:
            choice = int(str(choice).strip())
            if not choice in range(1,4):
                raise Exception
            break
        except Exception:
            print "Invalid Choice."

    if choice == 1:
        filePath = raw_input("Enter the CSV file path to process: ")
        processCsvDataDisplayResults(filePath)
        
    elif choice == 2:
        filePath = TEST_CSV_PATH
        processCsvDataDisplayResults(filePath)
        
    else:
        sys.exit(0)          
    print "Correct Choice"


def processCsvDataDisplayResults(filePath):
    sharesInfo = SharesInfo(filePath)
    sharesInfo.processCsvFile()
    displayMainMenu()
    
if __name__ == '__main__':
    main()
