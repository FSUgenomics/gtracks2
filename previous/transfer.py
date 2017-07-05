#!/usr/bin/env python

"""Goal:
    Transfer Tracks/rows from one Spreadsheet to Another.
    It will insert only fields that exist in Destination.
    User input: source destination spreadsheetID and tracks
    Example:
    ./transfer.py 138h...Yw   1-PTk...M_Us4  -t fam1_wig fam2_wig
"""
#transfer from one spreadsheet to the other
#note: only insert columns that match


import argparse
import os
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient import discovery

####GLOBAL VARIABLES
#arguments from argparse
ARGS = []

#credentials
SERVICE = None
#set with environment variable "export API_KEY=..." or use "-k" option
API_KEY = None
#necessary for writing
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "gtracks"

#holds read data
TRACK_COL = {}
TRACK_IND = {}
FIRST_ROW = {}

#default sheet and range
RANGE = "Sheet1"
RANGE_D = "Sheet1!"
RANGE_R = "Sheet1!1:1"

#IF NUMBER CONVERSION ERROR Occurs change to RAW
#VALUE_OPTION = "USER_ENTERED"
VALUE_OPTION = "RAW"


def main():

    #PARSE ARGUMENTS
    parseArgs()

    #LOGIN: creates object for making requests and prepares for writing to DST
    #create service objects to make requests
    googleLogin()

    #VALID: tracks, SRC, and DST sheets exist
    validArgs()

    #for each track
    for trck in ARGS.tracks[0]:
        #get row for that track from SRC
        row = getTrack(ARGS.src, trck)

        #clean the row
        row = cleanRow(row)

        #append the row to DST
        insertTrack(row)



"""
        LOGIN

                """
#login necessary to write to spreadsheet
def googleLogin():
    global SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME, SERVICE, API_KEY
    #scope limits the permissions of an OAUTH credential
    #file names local file containing credentials

    #check CLIENT_SECRET_FILE exists or provided as argument
    googleLoginHelper()

    #stores credentials into an object for later retrieval
    store = Storage(CLIENT_SECRET_FILE)

    #check if given API_key
    #REVIEW: not needed, need credentials for modifying
    loginAPIKey()

    #ensures expired or invalid credentials don't crash application
    try:
        credentials = store.get()
    except:
        credentials = False


    #if credentials invalid or expired, create new ones
    if not credentials or credentials.invalid:
        #secret file and scope

        #flow creates a temporary object that helps acquire needed credentials
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)

        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])

        #run_flow: runs through steps to acquire credentials
        credentials = tools.run_flow(flow, store, flags)

    #adds credentials to every HTTP request
    http = credentials.authorize(httplib2.Http())

    #specifies the API we will use
    discoveryUrl =\
        ('https://sheets.googleapis.com/$discovery/rest?version=v4')

    #build method constructs an object to interact with the API
    try:
        SERVICE = discovery.build('sheets', 'v4', http=http,
            discoveryServiceUrl=discoveryUrl, developerKey = API_KEY)
    except:
        print "Error: continuing without API_KEY"
        SERVICE = discovery.build('sheets', 'v4', http=http,
            discoveryServiceUrl=discoveryUrl)


#check the file path of credentials provided
def googleLoginHelper():
    global ARGS, CLIENT_SECRET_FILE

    #check and get credentials file
    #credentials argument provided?
    if ARGS.c is not None and os.path.isfile(os.path.abspath(ARGS.c)):
        #expand or make absolute
        CLIENT_SECRET_FILE = os.path.abspath(ARGS.c)
    #using default client_secret.json
    else:
        CLIENT_SECRET_FILE = os.path.join(os.getcwd(), CLIENT_SECRET_FILE)
        if not os.path.isfile(CLIENT_SECRET_FILE):
            print \
            "Error: validArgs No valid credentials file provided.\n\
            Please create a credentials file using Step 1: \n\
            https://developers.google.com/sheets/api/quickstart/python \n\
            rename it to 'client_secret.json' and save it in this directory \n\
            or use '-c' flag to specify a path to it"
            exit()

#check if key provided as arg or environment variable
def loginAPIKey():
    #API KEY NOT NEEDED
    global ARGS, API_KEY

    #check environment variable
    env_key = os.environ.get("API_KEY")

    if ARGS.k is not None:
        if len(ARGS.k) < 32:
            print "Error: API_KEY '-k' too short"
            return
        API_KEY = ARGS.k
    elif env_key is not None:
        if len(env_key) < 32:
            print "Error: API_KEY environment variable too short"
            return
        API_KEY = env_key
    #else leave API_KEY = None




#REVIEW: NO LONGER USED, NEED CLIENT_SECRET_FILE to write at all
#create global SERVICE object for requesting spreadsheet data
def makeService():
    global SERVICE, API_KEY
    #specifies the API we will use
    discoveryUrl =\
        ('https://sheets.googleapis.com/$discovery/rest?version=v4')

    #build method constructs an object to interact with the API
    SERVICE = discovery.build('sheets', 'v4',
        discoveryServiceUrl = discoveryUrl, developerKey = API_KEY)

"""

    PARSE ARGUMENTS

                    """

#parse arguments using argparse (src, dst, -t, credentials_path)
def parseArgs():
    global ARGS
    #PARSING ARGUMENTS
    #SRC
    parser = argparse.ArgumentParser()
    parser.add_argument("src",
     help="Enter SPREADSHEETID of source Spreadsheet", action="store")

    #DST
    parser.add_argument("dst",
     help="Enter SPREADSHEETID of destination Spreadsheet", action="store")

    #tracks
    #nargs allows this "-t track1 track2" instead of "-t track1 -t track2"
    parser.add_argument("-t","--tracks", nargs="*",
     help="Specify track(s) to copy", action="append")

    #credentials
    parser.add_argument("-c", "-credentials", help="Provide credentials JSON \
     file path. For instructions see Step 1: \
     https://developers.google.com/sheets/api/quickstart/python \
     use 'gtracks' as the application name.",action="store")

    #api key
    parser.add_argument("-k", "-key", help ="Enter API_KEY.")


    #errors on invalid arguments
    ARGS = parser.parse_args()

#check arguments are valid and they exist
def validArgs():
    global ARGS, CLIENT_SECRET_FILE

    #check dst != src
    if ARGS.src == ARGS.dst:
        print "Error: Source and Destination are the Same"
        exit()


    #check Existence of Source Spreadsheet
    if not sheetExists(ARGS.src):
        #error
        print "Error: Finding Source Spreadsheet '%s'" % ARGS.src
        exit()

    #check Existence of Destination SpreadSheet
    if not sheetExists(ARGS.dst):
        #error
        print "Error: Finding Destination SpreadSheet '%s'" % ARGS.dst
        exit()

    #check tracks exist in the SRC and not DST
    for t in ARGS.tracks[0]:
        #error
        if not trackExists(ARGS.src, t):
            print "Error: SRC Track %s Not Found" % t
            exit()
        if trackExists(ARGS.dst, t):
            print "Error: DST Track %s Overwriting\nCancelling operation..." % t
            exit()

### VALIDARGS HELPERS:

#checks existence of spreadsheet
def sheetExists(SHEETID):
    global SERVICE
    #check if both sheets exist?
    try:
        #try requesting the sheet
        results = SERVICE.spreadsheets().values().get\
            (spreadsheetId = SHEETID, range = RANGE_R ).execute()
        return True
    except:
        #unable to request the sheet
        return False

#check if track exists
def trackExists(SH_ID, track):
    #dictionaries
    global FIRST_ROW, TRACK_IND, TRACK_COL, SERVICE

    #service object already created

    #if already obtained, skip this part
    if SH_ID not in TRACK_COL.keys() or SH_ID not in TRACK_IND.keys():
        #get row containing the headers
        getRow(SH_ID, 1)

        #get column containing tracks
        getCol(SH_ID, "track")

    #check if track is contained in the column
    for em in TRACK_COL[SH_ID]["values"]:
        if track == em[0]:
            return True

    #not found
    return False

#trackExists Helper Functions
#gets the fields/column names of the sheet
def getRow(SH_ID, row_ind):
    global FIRST_ROW, SERVICE
    #find column index that contains track names
    row_range = RANGE_D + str(row_ind) + ":" + str(row_ind)

    #get it
    row = SERVICE.spreadsheets().values().get(spreadsheetId =
        SH_ID, range =row_range).execute()

    if row_ind == 1:
        #save the first row
        #gets the row containing fields/headers
        FIRST_ROW[SH_ID] = row

    return row


#gets track column
def getCol(SH_ID, colname):
    global TRACK_IND, TRACK_COL, SERVICE

    #which column contains the tracks?
    try:
        TRACK_IND[SH_ID] = FIRST_ROW[SH_ID][u"values"][0].index("track")
    except ValueError:
        print "Error: Spreadsheet '%s' does not contain 'track' \
            column" % SH_ID
        exit()

    #convert track column index to column letter
    TRACK_IND[SH_ID] = chr(ord("A") + TRACK_IND[SH_ID])

    #create query range string
    col_range  = RANGE_D + TRACK_IND[SH_ID] + ":" + TRACK_IND[SH_ID]

    #get column containing track names, save globally
    TRACK_COL[SH_ID] = SERVICE.spreadsheets().values().get(spreadsheetId =
        SH_ID, range=col_range).execute()


"""

    INSERTING TRACKS

                    """

#get row for that track
def getTrack(SH_ID, track):
    global SERVICE, TRACK_COL

    #flattening list of lists
    flat_lst = [el for subl in TRACK_COL[SH_ID]["values"] for el in subl]

    #find the track within the column
    try:
        row_ind = flat_lst.index(track)+1
    except ValueError:
        print "Error: Spreadsheet %s does not contain '%s' track" \
            % (SH_ID, track)
        exit()

    #range containing track
    row_range = RANGE_D + str(row_ind) + ":" + str(row_ind)

    #get track using the range
    return SERVICE.spreadsheets().values().get(spreadsheetId = SH_ID,
        range = row_range).execute()


def insertTrack(row):
    global FIRST_ROW, SERVICE, ARGS, API_KEY
    #if field match insert value, else move to next field

    #insert it
    result = SERVICE.spreadsheets().values().append(spreadsheetId = ARGS.dst,
        range = RANGE, valueInputOption= VALUE_OPTION, body = row,
        key = API_KEY).execute()


#returns row to insert in valueRangeObject format
def cleanRow(rowToclean):
    #fields in dst
    global FIRST_ROW
    #creat a row!
    temp_row = []

    #for each column in DST
    for col_name in FIRST_ROW[ARGS.dst][u"values"][0]:
        #find corresponding in SRC
        try:
            ind = FIRST_ROW[ARGS.src][u"values"][0].index(col_name)
            temp_row.append(rowToclean[u"values"][0][ind])
        #if no corresponding column in SRC then add NA
        except ValueError:
            temp_row.append("NA")


    #object to insert
    value_range_obj = {u"range": RANGE,
     u"values": [temp_row], u"majorDimension": u"ROWS"}

    return value_range_obj




if __name__ == "__main__":
    main()
