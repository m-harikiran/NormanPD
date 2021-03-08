# CS 5293, Spring 2021 Project 0

##### Author: Harikiran Madishetti

---

## About

In this project we will learn to use python, UNIX commands, Git and SQLite3 to read data from websites or CSV or pdf files, then process the data and finally storing it in the database for analysis. For this I have used the incidents data provided by [Norman Police Department](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/daily-activity-reports 'Norman Police Department')

## Packages Required

The below is the list of packages used in this project.

- urllib
- tempfile
- PyPDF2
- sqlite3
- re
- prettytable
- argparse
- validators

Libraries such as argparse, tempfile, sqlite3, re, and urllib are standard libraries in python3. To install other libraries please use Command `pipenv install -r requirements.txt`

## Assumptions

After analyzing multiple incident reports provided by the Norman Police Department, for this project I have assumed that the data is free of NULL values or fields. So, if there is any NULL value for an incident in report then the final results may not be appropriate.

## Description

In this project I have downloaded the incidents data from Norman Police Department and then parsed it and stored it database to fetch nature of incidents and their respective count. To implement this the project package has two main files:
**1. main.py**
**2. project0.py**
In order to test the package we also have **test_project0.py**.

### main.py

This file is invoked to process the data and output the results. This files takes the input parameters **-- incidents** as **URL** containing the list of incidents for a particular day.

The main function has methods imported from **project0.py** which are used to download, store the data in the database and then fetch the summary of inserted data. The below are different methods called by main function:

- Method `project0.fetchIncidents()` is used to fetch the incidents data from url provided
- Method `project0.extractIncidents()` is used to parse the data obtained from the website and store it in list format to easily insert it into the database
- Method `project0.createDB()` is used to create a new database
- Method `project0.populateDB()` is used to insert the parsed data into the database
- Method `project0.status()` is used to fetch the summary of incidents from the database tables
