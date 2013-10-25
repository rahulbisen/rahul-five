PROBLEM STATEMENT
=============================
      Task
-------------------------------------------------------------------------------------------------------------------
Consider Share prices for a N number of companies given for each month since year     
         1990 in a CSV file.  Format of the file is as below with first line as header.
 
Year,Month,Company A, Company B,Company C, .............Company N
1990, Jan, 10, 15, 20, , ..........,50
1990, Feb, 10, 15, 20, , ..........,50
.
.
.
.
2013, Sep, 50, 10, 15............500
 

a) List for each Company year and month in which the share price was highest.

b) Submit a unit test with sample data to support your solution.   

-------------------------------------------------------------------------------------------------------------------

SOLUTION STATEMENT:
=============================
      The tool/program for the problem statement mentiond is written in python. Below are the details.

-------------------------------------------------------------------------------------------------------------------
1) Specification:
-----------------------------
Language: Python
Language Version: Python 2.7.5
Platform: Created on windows. Tested on Unix RHEL-6 and Windows 7 starter edition. should work seemlessly on both.

2) Modules/Files Definition:
-----------------------------
2.1) company_shares.py
      Defines all the classes and methods required for processing CSV data and printing results.

2.2) process_csv.py
      This is the main python app that invokes classes and methods from company_shares.py and presents a menu to
       the user to do variety of tasks.

2.3) company_shares_test.py
      Defines 26 testcases to perform unittests for the module company_shares.py

2.4) test_data.csv
      Test CSV file created with sample test data.

2.5) other CSV files
      There are other CSV files in the tool's directory to test various cases for manual testing/debugging.

3) Technical Problems/Issues:
-----------------------------
3.1) One of the test cases in 'company_shares_test.py', TestCompanyShares.testCheckCsvPathWithUnreadableFile
      fails only on windows as it is difficult, not impossible, to make a file unreadable through the python 
      'os.chmod' method. However, this happens seamlessly on Unix and the test passes. 
      Need more time to look into it. For now, the test gets skipped when run from windows desktop.
      
4) End
-------------------------------------------------------------------------------------------------------------------
