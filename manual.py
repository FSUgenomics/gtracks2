#!/usr/bin/env python

#REVIEW: description
"""Description"""

import argparse
import os
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient import discovery


#GLOBAL VARIABLES
ARGS = []

#data to insert
ROW = []

#credentials
SERVICE = None
#necessary for writing
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "gtracks"


#default sheet and range
RANGE = "Sheet1"
RANGE_R = "Sheet1!1:1"

#IF NUMBER CONVERSION ERROR Occurs change to RAW
#VALUE_OPTION = "USER_ENTERED"
VALUE_OPTION = "RAW"

def main():
    #PARSE ARGUMENTS
    parseArgs()

    print "ARGS.row = %s" % (ARGS.row)

    #login in
    googleLogin()

    #check arguments
    if not sheetExists(ARGS.dst):
        print "Error: %s provided SheetID not found" % ARGS.dst
        exit()


    #insert provided data
    insertRow()

#allow credentials and sheetID
def parseArgs():
    global ARGS
    parser = argparse.ArgumentParser()

    #add destination
    parser.add_argument("dst", help="Enter destination SpreadSheetID",
        action = "store")

    #row info
    parser.add_argument("row", help="Enter row content", nargs="*",
        action = "store")

    #add credentials
    parser.add_argument("-c", "-credentials",
        help = "Provide credentials JSON file path. For instructions\
        see Step1: \https://developers.google.com/sheets/api/quickstart/python \
        use 'gtracks' as the application name", action="store")

    #REVIEW: allow flag for row number
    #location to insert?

    ARGS = parser.parse_args()

#create service object for requests
def googleLogin():
    global SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME, SERVICE

    #check CLIENT_SECRET_FILE exists or provided as argument
    googleLoginHelper()

    #stores credentials into an object for later retrieval
    store = Storage(CLIENT_SECRET_FILE)

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
            discoveryServiceUrl=discoveryUrl)
    except:
        print "Error: unable to build Service object"
        exit()


#find credentials
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


#check provided dst sheetid
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


#construct value range object and insert it
def insertRow():
    global ARGS, SERVICE, VALUE_OPTION

    value_range_obj = {u"range": RANGE,
        u"values": [ARGS.row], u"majorDimension": u"ROWS"}


    result = SERVICE.spreadsheets().values().append(spreadsheetId = ARGS.dst,
        range = RANGE, valueInputOption= VALUE_OPTION,
        body = value_range_obj).execute()





if __name__ == "__main__":
    main()
