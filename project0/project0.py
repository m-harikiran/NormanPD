import urllib.request
import tempfile
import PyPDF2
import sqlite3
import re
from prettytable import from_db_cursor

# Downloading Data


def fetchIncidents(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    # HTTP request error handling
    try:
        data = urllib.request.urlopen(
            urllib.request.Request(url, headers=headers))
        return data
    except urllib.error.HTTPError as err:
        # Printing Error Message
        print('\n', err, '\nPlease check the url and try again\n')
        quit()  # If error occurs then application will be terminated

# Extracting the data from downloaded file


def extractIncidents(incident_data):

    # Creating a temporary file to store the data
    tf = tempfile.TemporaryFile()

    # Write the pdf data to a temp file
    tf.write(incident_data.read())

    # setting the cursor of the file to start
    tf.seek(0)

    # Reading the PDF
    pdfReader = PyPDF2.pdf.PdfFileReader(tf)
    # Getting the total page numbers in PDF
    pdfPageNumbers = pdfReader.getNumPages()

    # Extracting the text from page
    pdfData = pdfReader.getPage(0).extractText()

    # Iterating through remaining pages and appending data
    for i in range(1, pdfPageNumbers):
        pdfData += pdfReader.getPage(i).extractText()

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

# Connecting to a Dababase and creating a table


def createDB():

    dbName = 'normanpd.db'  # Name of the database where the data should be inserted

    # All the files will be saved in normanpd.db
    conn = sqlite3.connect(dbName)

    # Creating a cursor object to execute SQL commands
    cur = conn.cursor()

    # Dropping the table if it exists
    cur.execute('''DROP TABLE IF EXISTS incidents''')

    # Creating table
    cur.execute('''CREATE TABLE IF NOT EXISTS incidents 
                      (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT)''')

    conn.commit()  # To save changes in db

    conn.close()  # Closing the connection to db

    return dbName

# Inserting data in the Database


def populateDB(dbName, incidents):

    # All the files will be saved in normanpd.db
    conn = sqlite3.connect(dbName)

    # Creating a cursor object to execute SQL commands
    cur = conn.cursor()

    # Inserting the records into database
    cur.executemany('''INSERT INTO incidents VALUES(?,?,?,?,?)''', incidents)

    conn.commit()  # To save changes in db

    conn.close()  # Closing the connection to db

# Fetching results from Database


def status(dbName):

    # All the files will be saved in normanpd.db
    conn = sqlite3.connect(dbName)

    # Creating a cursor object to execute SQL commands
    cur = conn.cursor()

    # Selecting the results from DB
    cur.execute('''SELECT nature as'Incidents_Nature', count(*) as 'Incidents_Count' from incidents 
                          GROUP BY nature 
                          ORDER BY nature''')

    # Printing all the records fetched from DB as per criteria
    # print('''\n*************************************
    #          \nIncidents_Nature  |  Incidents_Count
    #          \n*************************************''')
    # for i in cur.fetchall():
    #     print('*',i[0], '|', i[1])

    # Printing all the records fetched from DB as per criteria
    # print('\n'+ tabulate(cur.fetchall(), headers=[
    #       'Incidents_Nature', 'Incidents_Count'], tablefmt='orgtbl') + '\n')

    # Fetching the results from databse and storing it into pretty table object
    incidentsTable = from_db_cursor(cur)

    # Aligning the Incidents_Nature Column to Left
    incidentsTable.align['Incidents_Nature'] = 'l'

    # Aligning the Incidents_Count Column to Center
    incidentsTable.align['Incidents_Count'] = 'c'

    # Printing the results obtained from DB in tabular format where each attribute is seperated by |
    print('\n', incidentsTable, '\n')

    # print('*************************************')
    conn.close()  # Closing the connection to db
