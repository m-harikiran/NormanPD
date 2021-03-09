from project0 import project0
import sqlite3
import os
import PyPDF2
import re

# Incidents URL for teesting
pdfURL = 'https://www.normanok.gov/sites/default/files/documents/2021-03/2021-03-01_daily_incident_summary.pdf'

# Testing Fetch Incidents


def testFetchIncidents():
    data = project0.fetchIncidents(pdfURL)  # Fetching the data from url
    assert data is not None  # Asserting if data is object is enpty or not

# Testing Extracted data


def testExtractIncidents():
    incidents_data = project0.fetchIncidents(pdfURL)

    incidentsList = project0.extractIncidents(incidents_data)

    # Checking if return type is list or not
    assert type(incidentsList) is list
    assert len(incidentsList) != 0  # Checking if list is empty or not

    for items in incidentsList:
        assert len(items) == 5  # Checking the length of each incident

# Testing Database Creation


def testCreateDB():

    project0.createDB()  # Calling method to create db

    # Checking if the Database File is created or not.
    assert os.path.isfile('normanpd.db')

    conn = sqlite3.connect('normanpd.db')  # Connecting to database

    cur = conn.cursor()  # Connection cursor to execute statements

    cur.execute(
        '''select * From incidents''')  # Executes query if table exists else throws error

    assert cur.fetchall() == []  # Checks if the newly created table is empty or not


def testPopulateBD():
    # Download data
    incident_data = project0.fetchIncidents(pdfURL)

    # Extract data
    incidentsList = project0.extractIncidents(incident_data)

    # Create new database and create table
    dbName = project0.createDB()

    # Insert data into incidents table
    project0.populateDB(dbName, incidentsList)

    # All the files will be saved in normanpd.db
    conn = sqlite3.connect(dbName)

    # Creating a cursor object to execute SQL commands
    cur = conn.cursor()

    cur.execute('''select count(*) from incidents''')

    # Checking if the all the data is inserted into database or not
    assert len(incidentsList) == cur.fetchall()[0][0]

# Method to extract PDF data


def pdfData():
    pdfReader = PyPDF2.pdf.PdfFileReader(
        '2021-03-01_daily_incident_summary.pdf')

    # Extracting the text from page
    pdfData = pdfReader.getPage(0).extractText()

    # Cleaning the data extracted from pdf

    # Handling columns with multi-line data
    pdfData = pdfData.replace(' \n', ' ')

    # Spliting the data based on date
    pdfData = re.split(r'\s+(?=\d?\d?\/\d?\d?\/\d{4} \d?\d?:\d?\d?)', pdfData)

    pdfDataList = []

    # Range starting from 1 as first element in list is names of columns/attributes
    for i in range(1, len(pdfData)-1):
        l = pdfData[i].split('\n')

        # Checking and removing unwanted cells ('Title of PDF file')
        while len(l) > 5:
            l.pop()

        # Appending to list only if the length of list is equal to 5 i.e. No. of attributes in pdf
        if len(l) == 5:
            pdfDataList.append(l)

    return pdfDataList


def testStatus():
    # Reading the PDF
    incidentsList = pdfData()

    # Create new database and create table
    dbName = project0.createDB()

    # Insert data into incidents table
    project0.populateDB(dbName, incidentsList)

    conn = sqlite3.connect(dbName)

    # Creating a cursor object to execute SQL commands
    cur = conn.cursor()

    # Selecting and Concatenating the results from DB
    cur.execute('''SELECT sum(Incidents_count) 
                            from (SELECT nature as'Incidents_Nature', count(*) as 'Incidents_Count' 
                                                        from incidents group by nature) a''')

    # Verifying if the count of incidents reported with final results from status()
    assert len(incidentsList) == cur.fetchall()[0][0]
