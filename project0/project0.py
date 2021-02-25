import urllib
import tempfile
import PyPDF2
import sqlite3
import re

#Downloading Data
def fetchincidents(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"                          
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers))

    return data

#Extracting the data from downloaded file
def extractincidents(incident_data):
    
    #Creating a temporary file to store the data
    fp = tempfile.TemporaryFile()

    # Write the pdf data to a temp file
    fp.write(incident_data.read())

    #setting the cursor of the file to start
    fp.seek(0)

    #Reading the PDF
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    pageNumbers = pdfReader.getNumPages()   #Getting the total page numbers in PDF

    pdfData = pdfReader.getPage(0).extractText() #Extracting the text from page

    #Iterating through remaining pages and appending data
    for i in range (1, pageNumbers):
        pdfData += pdfReader.getPage(i).extractText()
    
    #Cleaning the data extracted from pdf

    pdfData = pdfData.replace(' \n', ' ')  #Handling columns with multi-line data

    pdfData = re.split( r'\s+(?=\d?\d?\/\d?\d?\/\d{4} \d?\d?:\d?\d?)' , pdfData) #Spliting the data based on date

    pdfDataList = []  
    
    for i in range(1, len(pdfData)-1):
        l = pdfData[i].split('\n')
        
        #Checking and removing unwanted cells
        while len(l) > 5:
            l.pop()
        
        pdfDataList.append(l)
    
    return pdfDataList