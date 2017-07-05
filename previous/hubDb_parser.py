
"""
CHANGE THE FOLLOWING TO USE:
FILEURL <== text file
CLIENT_SECRET_FILE <== credentials JSON (see DEPENDENCIES)
APPLICATION_NAME <== didn't actually use
SPREADSHEETID <== example url everything after d/ but before edit "
"""

"""
DEPENDENCIES:

Uses Python 2.7
Install Google Client Library `pip install --upgrade google-api-python-client`
Create Spreadsheet Credentials: https://developers.google.com/sheets/quickstart/python
Download Credentials and Place in same directory (name "client_secret.json")
"""



import urllib
import os
"""GOOGLE AUTHENTICATION"""
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage




"""GLOBAL VARIABLES"""
ALLSTANZAS = []
NA = "NA"
FILEURL = "http://www.bio.fsu.edu/~dvera/hubs/eveland/zeaMay_b73_v3/hubDb.txt"
#HACK:
FILENAME = ""
SCOPES = "https://www.googleapis.com/auth/drive" #set of operations permitted
CLIENT_SECRET_FILE = "client_secret.json" #uniquely id application
APPLICATION_NAME = "Google Sheets API Cruise"
CRED_JSON = "sheets.google.com-cruise.json"
SPREADSHEETID = "1-8WD5eUWeACTzraeEFeNQ1A54pyl_iecyKBxk69DJIw"

REFERENCE_LIST = []

REF_DICT_INDEX = {}


"""DOWNLOADING AND READING FILE"""
#downloadsa local copy
def download():
    global FILENAME;
    #filename (everything after last '/')
    FILENAME = FILEURL.split('/')[-1]
    #copy locally (if it doesn't already exist)
    urllib.urlretrieve(FILEURL, FILENAME)


#reads file line by line, and appends to list
def readFile():
    global ALLSTANZAS, FILENAME
    with open(FILENAME, 'r') as file:
        stanza = []
        for line in file:
            if line == '\n':
                #ALLSTANZAS list of dictionaries
                ALLSTANZAS.append(parseStanza(stanza))
                stanza = []
                continue
            else:
                #rstrip removes newline from end
                stanza.append(line.rstrip())

#stanza into a list containing text after field
def parseStanza(stanza):
  # print "**?**\nstanza = %s" % stanza
  global REFERENCE_LIST;
  row_l = [NA] * len(REFERENCE_LIST)
  row_l[0] = -1

  #for each line in stanza
  for line in stanza:
      #find corresponding field
      pre_space = line.split(" ",1)[0]
      post_space = "".join(line.split(" ", 1)[1:])
      if(pre_space in REFERENCE_LIST):
          #append after the field
          row_l[REF_DICT_INDEX[line.split(" ",1)[0]]] = post_space
          if(line.split(" ",1)[0] == "bigDataUrl"):
              prefix_separated = post_space.split("/", 1)
              row_l[REF_DICT_INDEX["_urlPrefix"]] = prefix_separated[0] + "/"
              row_l[REF_DICT_INDEX["_fileName"]] = prefix_separated[1]

  return row_l


"""GOOGLE RELATED
NEED MAJOR CLEANUP
"""
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
    global REFERENCE_LIST, REF_DICT_INDEX
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http = http,
    discoveryServiceUrl = discoveryUrl)

    results = service.spreadsheets().values().get(spreadsheetId = SPREADSHEETID,
     range ="Sheet1!1:1" ).execute()
    #REFERENCE_LIST = results{"values"}[0]
    i = 0
    for el in results["values"][0]:
        s =  el.encode('ascii', 'ignore')
        print "normal = %s " % s
        REFERENCE_LIST.append(s)
        REF_DICT_INDEX[s] = i
        i = i + 1



#appending the list value from above in column order
#very confusing
def appendRows(http):
    global ALLSTANZAS
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4',
     http = http,discoveryServiceUrl = discoveryUrl)

    body = {"range": 'A1', "majorDimension":"ROWS", "values": ALLSTANZAS}
    result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEETID,
    range = "A1", valueInputOption ="USER_ENTERED", body = body).execute()


def main():
    print ("entering main")
    # Google login
    http = loginGoogle()
    #get fields and place in REFERENCE_LIST
    getFields(http)

    download()
    readFile()
    #append to drive spreadsheet
    appendRows(http)




main()
