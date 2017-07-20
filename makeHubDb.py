#!/usr/bin/env python


import gspread
import argparse
import exceptions
#local
import utility as util

HEADER_ROW = ["hub_name", "hubId", "hub.txt url", "user/host",
            "path to hub directory"]

FILE_SAVE = ".hubDbId"
HUBDB_NAME = "_hubDb"
SHEETID = None


def makeHubDbMain(AUTH_GSPREAD_OBJ, ARGS):
    global HEADER_ROW
    #gspread object created already

    #does hubDbID already exists
    try:
        open(FILE_SAVE, "r")
        #opened successfuly?
        print "\
        makeHubDb Error: %s already exists" % FILE_SAVE
        getHubDbSheetId()
        printURL(None)
        exit()

    except IOError:
        #it doesn't exist, so we can continue
        pass

    #create the sheet (exits if error occurs)
    # spsheet = util.createSheet(AUTH_GSPREAD_OBJ, ARGS.hubDbname)
    spsheet = util.createSheet(AUTH_GSPREAD_OBJ, HUBDB_NAME)

    #insert fields in first column
    util.insertRow(AUTH_GSPREAD_OBJ,spsheet, "A1", HEADER_ROW)

    #save the spreadsheet id to FILE_SAVE
    saveHubDbSheetID(spsheet)

    #print the url
    printURL(spsheet)

#save the spreadsheetID of the new spreadsheet
def saveHubDbSheetID(spsheet):
    global FILE_SAVE

    with open(FILE_SAVE, 'w') as f:
        f.write(spsheet.id)

#returns the sheetID from hubDbId
def getHubDbSheetId():
    global FILE_SAVE, SHEETID

    with open(FILE_SAVE, 'r') as f:
            SHEETID = f.readline()


def printURL(spsheet):
    global SHEETID
    if SHEETID is not None:
        url = "https://docs.google.com/spreadsheets/d/"+SHEETID
    else:
        #create url
        url = "https://docs.google.com/spreadsheets/d/"+spsheet.id

    #alternative url
    print "\
    Your _hubDb google sheet can be found here: \n%s" % url
