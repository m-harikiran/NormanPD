# Norman Police Department Incidents Summary

#### Author: Harikiran Madishetti

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
- os
- prettytable
- argparse
- validators

Libraries such as argparse, tempfile, sqlite3, re, os, and urllib are standard libraries in python3. To install other libraries please use Command `pipenv install -r requirements.txt`

## Assumptions

After analyzing multiple incident reports provided by the Norman Police Department, for this project I have assumed that the data is free of NULL values or fields. So, if there is any NULL value for an incident in report then the final results may not be appropriate.

## Description

In this project I have downloaded the incidents data from Norman Police Department and then parsed it and stored it database to fetch nature of incidents and their respective count. To implement this the project package has two main files:
**1. main.py**
**2. project0.py**
In order to test the package we also have **test_project0.py**.

### 1. main.py

This file is invoked to process the data and output the results. This files takes the input parameters **-- incidents** as **URL** containing the list of incidents for a particular day.

The main function has methods imported from **project0.py** which are used to download, store the data in the database and then fetch the summary of inserted data. The below are different methods called by main function:

- Method **`project0.fetchIncidents()`** is used to fetch the incidents data from url provided
- Method **`project0.extractIncidents()`** is used to parse the data obtained from the website and store it in list format to easily insert it into the database
- Method **`project0.createDB()`** is used to create a new database
- Method **`project0.populateDB()`** is used to insert the parsed data into the database
- Method **`project0.status()`** is used to fetch the summary of incidents from the database tables

### 2. project0.py

This package is used by **main.py** to fetch, extract data, and populate and fetch results from the database.

#### i. fetchIncidents(url)

This method takes input parameters as URL and urllib package is used to read the data from the given URL. This function returns the data that we have fetched from the URL. If there is an error in accessing the data from the URL then the function raises an error and exits the program.

#### ii. extractIncidents(incident_data)

This method takes the input parameters incident_data that we have fetched from the URL and is used to parse the data and finally store incidents in list format.

In this method I have used PyPDF2 to read the pdf data fetched from the URL. After reading the data, I have consolidated the data available in all the pages of the PDF to a string(**pdfData**).
In the **pdfData** each field is separated by **'\n'** .

##### Handling Multi-Line Data

In **pdfData** string multi-line data is separated by ' \n'. So I have replaced it with empty space(' ')

```python
pdfData = pdfData.replace(' \n', ' ')
```

##### Extracting Incidents

After handling the multi-line data, to extract each incident from **pdfData** I have considered splitting the data further based on the incident date/time field, as this was the easiest way to identify each incident.

```python
pdfData = re.split(r'\s+(?=\d?\d?\/\d?\d?\/\d{4} \d?\d?:\d?\d?)', pdfData)
```

##### Extracting Attributes of Incident

Once the data is split into each incident, we had strings of incidents, in which incidents attributes were separated by **'\n'**. I have then extracted attributes of each incident by splitting it w.r.t **'\n'**.

While extracting the Attributes of Incidents, I have noticed that some incidents have more than 5 attributes. The additional attributes were title, sub-title of the report and it's date of generation.

###### Handling Unwanted Attributes

If the length of the incident list is > 5 then I have removed the last elements from the list. I have removed last element as we have initially split the data into rows with respect to date. And finally, if the length of the incidents list is equal to 5 then I am appending the incidents to final list **pdfDataList** and returning it.

```python
for i in range(1, len(pdfData)-1):
	l = pdfData[i].split('\n')
# Checking and removing unwanted cells ('Title of PDF file')
	 while len(l) > 5:
		l.pop()
# Appending to list only if the length of list is equal to 5 i.e. No. of attributes in pdf
	if len(l) == 5:
		pdfDataList.append(l)
```

#### iii. createDB()

This methods takes no input parameters and this is used to create a database **normanpd.db** and create a table called **INCIDENTS** in it. Once the database and table is created this methods returns **dbName**.

The below is the snippet of code used to create table Incidents.

```python
cur.execute('''CREATE TABLE IF NOT EXISTS incidents
                      (incident_time TEXT, incident_number TEXT, incident_location TEXT,
					  nature TEXT, incident_ori TEXT)''')
```

#### iv. populateDB(dbName, incidents)

This methods takes database name, incidents list (returned by extractIncidents()) as input parameters and inserts the data into the database table incidents.

The below is the Snippet of code used to insert the data into the database.

```python
cur.executemany('''INSERT INTO incidents VALUES(?,?,?,?,?)''', incidents)
```

#### v. status(dbName)

This method takes database name as input parameter and fetches the summary of the incidents which are stored in the database table Incidents.

The below is the snippet of code used to fetch the summary of Incidents.

```python
cur.execute('''SELECT nature as'Incidents_Nature', count(*) as 'Incidents_Count' from incidents
                          GROUP BY nature
                          ORDER BY nature''')
```

Once the data is fetched from the database, the results are printed to the console in tabular format using **prettytables**.

```python
incidentsTable = from_db_cursor(cur)	# Fetching the results from databse and storing it into pretty table object
incidentsTable.align['Incidents_Nature'] = 'l'	 # Aligning the Incidents_Nature Column to Left
incidentsTable.align['Incidents_Count'] = 'c'	 # Aligning the Incidents_Count Column to Center
print('\n', incidentsTable, '\n') 	# Printing the results obtained from DB in tabular format where each attribute is seperated by |
```

### 3. test_project0.py

The package **test_project0.py** has test cases defined as methods, that can be used for unit testing of methods defined in the package **project0.py**. In order to test each method in **project0.py**, first we need to import **project0.py**.

#### i. testFetchIncidents()

This method is used to test method **fetchIncidents(url)** in **project0.py**. In this, I am verifying if the object returned by **project0.fetchIncidents(url)** when it is called is None or not.

```python
data = project0.fetchIncidents(pdfURL)  # Fetching the data from url
assert data is not None  # Asserting if data is object is enpty or not
```

#### ii. testExtractIncidents()

This method is used to test method **extractIncidents(incident_data)** in **project0.py**. In this method I am verifying weather the returned datatype of the method extractincidents() is list or not, verifying weather the returned list is not empty and finally checking if the there are exactly 5 attributes in each incident.

```python
assert type(incidentsList) is list	# Checking if return type is list or not
assert len(incidentsList) != 0 		# Checking if list is empty or not
for items in incidentsList:
	assert len(items) == 5		# Checking the length of each incident
```

#### iii. testCreateDB()

This method is used to test method **createDB()** in **project0.py**. In this method, I am verifying if the method created a database by looking for the database 'normanpd.db' file in the current directory of the project, and incidents table creation is verified by fetching results from the table.

```python
assert os.path.isfile('normanpd.db')		# Checking if the Database File is created or not.
conn = sqlite3.connect('normanpd.db')		# Connecting to database
cur = conn.cursor()				# Connection cursor to execute statements
cur.execute('''select * From incidents''')	# Executes query if table exists else throws error
assert cur.fetchall() == []			# Checks if the newly created table is empty or not
```

#### iv. testPopulateBD()

This method is used to test method **populateDB(dbName, incidents)** in **project0.py**. In this method I am verifying weather all the incidents returned by **extractIncidents()** are inserted properly into the database incidents table.

```python
cur.execute('''select count(*) from incidents''')	#SQL query to select count of inserted records
assert len(incidentsList) == cur.fetchall()[0][0]
```
