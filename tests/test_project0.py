from project0 import project0
import sqlite3

# Incidents URL for teesting
pdfURL = 'https://www.normanok.gov/sites/default/files/documents/2021-03/2021-03-01_daily_incident_summary.pdf'

# Testing Fetch Incidents


def testFetchIncidents():
    data = project0.fetchIncidents(pdfURL)  # Fetching the data from url
    assert data is not None  # Asserting if data is object is enpty or not

# Testing Extracted data


def testExtractIncidents():
    data = project0.fetchIncidents(pdfURL)

    incidentsList = project0.extractIncidents(data)

    # Checking if return type is list or not
    assert type(incidentsList) is list
    assert len(incidentsList) != 0  # Checking if list is empty or not

    for items in incidentsList:
        assert len(items) == 5  # Checking the length of each incident

# Testing Database Creation


def testCreateDB():

    dbName = project0.createDB()
    assert dbName == 'normanpd.db'  # Checking if created Database name


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

    cur.execute('''select * from incidents''')

    assert len(cur.fetchall()) > 1     #Checking if the data is inserted into database or not