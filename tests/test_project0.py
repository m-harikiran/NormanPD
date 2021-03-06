from project0 import project0

#Incidents URL for teesting
pdfURL = 'https://www.normanok.gov/sites/default/files/documents/2021-03/2021-03-01_daily_incident_summary.pdf'


def testFetchIncidents():
    data = project0.fetchIncidents(pdfURL)   #Fetching the data from url
    assert data is not None                   #Asserting if data is object is enpty or not

def testExtractIncidents():
    data = project0.fetchIncidents(pdfURL)
    
    incidentsList = project0.extractIncidents(data)

    assert type(incidentsList) is list  #Checking if return type is list or not
    assert len(incidentsList) != 0      #Checking if list is empty or not
    
    for items in incidentsList:
        assert len(items) == 5          #Checking the length of each incident
    