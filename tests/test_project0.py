from project0 import project0

#Incidents URL for teesting
pdfURL = 'https://www.normanok.gov/sites/default/files/documents/2021-03/2021-03-01_daily_incident_summary.pdf'


def testFetchIncidents():
    data = project0.fetchIncidents(pdfURL)
    assert data is not None

def testExtractIncidents():