#!/usr/bin/env python


import gspread
import argparse
#local
import utility as util

HEADER_ROW = ["hub_name", "hubId", "hub.txt url", "user/host",
            "path to hub directory"]

FILE_SAVE = ".hubDbId"


def makeHubDbMain(AUTH_GSPREAD_OBJ, ARGS):
    global HEADER_ROW
    #gspread object created already

    #create the sheet (exits if error occurs)
    spsheet = util.createSheet(AUTH_GSPREAD_OBJ, ARGS.hubDbname)

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

def printURL(spsheet):
    #create url
    url = "https://docs.google.com/spreadsheets/d/"+spsheet.id
    #alternative url
    #url = "https://drive.google.com/drive/search?q="+spsheet.title
    print url
