#Goal:
#Read from Google Spreadsheet and Post write text file.


"""
Testing:
1)
Need text file identical to spreadsheet.
To compare my output.
Currently diff, and get some differences.

2)
Produce spreadsheet from text file.
Use this script to produce text file.
Compare both text files.
"""


import urllib
import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#GLOBAL Variables
filename = "hubDb.txt"
header_Row = []
all_Rows = []


SCOPES = "https://www.googleapis.com/auth/drive" #set of operations permitted
CLIENT_SECRET_FILE = "client_secret_reverse.json" #uniquely id application
APPLICATION_NAME = "Google Sheets Reverse"
CRED_JSON = "sheets.reverse.json"
SPREADSHEETID = "19_uhaREmARanEMk2fUhgWjcWGcC3WSaWsOM-EzhfJJM"


def loginGoogle():
    #modified version of Google api Demo

    #prepare path to obtain credentials
    cred_dir = os.path.join(os.getcwd(), '.credentials')

    #create it if it doesn't exist
    if not os.path.exists(cred_dir):
        os.makedirs(cred_dir)
    #create file for this
    cred_path = os.path.join(cred_dir, CRED_JSON)

    #create instance of Storage class to retrieve credentials object
    store = Storage(cred_path)
    #get credentials from Storage object
    credentials = store.get()


    #check the credentials!
    if not credentials or credentials.invalid:
        #oath create flow object <== store id, secret and OAuth params
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        #user_agent used by client applications residing in the device
        #reveal info about the device + software visitor using
        #software that acts as a bridge btwn me and the internet/service
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)


    #authorize the credentials
    return credentials.authorize(httplib2.Http())
    #httplib2 is a comprehensive HTTP client library
    #Http represents a client HTTP interface
    #now we are ready to start inserting rows!

def getFields(http):
    global header_Row, all_Rows;
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4',
     http = http,discoveryServiceUrl = discoveryUrl)
    #I just get the first row!!
    results = service.spreadsheets().values().get(spreadsheetId = SPREADSHEETID,
     range ="Sheet1" ).execute()
    #what happens if the results are empty?

    #REFERENCE_LIST = results{"values"}[0]
    print results["range"]
    print len(results["values"][0])
    print "result = %s" % results

    for el in results["values"]:
        l = [x.encode('ascii', 'ignore') for x in el]
        header_Row = l
        break;
    print "header_Row = %s" % header_Row
    del results["values"][0]

    for el in results[u'values']:
        # s =  el.encode('ascii', 'ignore')
        l = [x.encode('ascii', 'ignore') for x in el]
        all_Rows.append(l)

def writeFile():
    global header_Row, all_Rows, filename;
    #open the file to write to
    #HACK: append to a string first, then write the entire string?
    f = open(filename, 'w');
    for i in range(len(all_Rows)):
        for j in range(len(all_Rows[i])):
            if(all_Rows[i][j] == "NA"):
                continue
            elif(header_Row[j][0] == '_'):
                continue;
            else:
                f.write("%s %s\n" % (header_Row[j], all_Rows[i][j]))
        f.write("\n")


getFields(loginGoogle())
writeFile()
