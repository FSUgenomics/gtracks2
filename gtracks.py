
""" Main:
    1. Get Credentials (authorized gspread object)
    2. Parse Arguments
    3. Call Appropriate script (makeHubDb, addHub, etc)
    Script then Checks Arguments and Runs
"""

#TODO: add subparsers!!
#TODO: how will user obtain application credentials?
#BUG: -c must be provided at the very beginning for main parser to see it
#BUG: else will have to add it do each subparser?
#TODO: add more scripts

import os
import sys
import argparse
#Local modules
import credentials as cred
import makeHubDb
import addHub


APPLICATION_CREDENTIALS = None
ARGS = None

def main():
    global APPLICATION_CREDENTIALS

    #parse arguments
    args = argParseMain()

    #check if APPLICATION_CREDENTIALS provided
    getCredentialsArg()

    #get authorization object
    AUTH_GSPREAD_OBJ = cred.authorizeGS(APPLICATION_CREDENTIALS)

    #call appropriate script!
    selectScript(AUTH_GSPREAD_OBJ)

#parsing each possible subcommand using subparsers
def argParseMain():
    global AVAILABLE_SCRIPTS, ARGS

    #gtracks parser
    parser = argparse.ArgumentParser(prog="gtracks")
    parser.add_argument("-c", "-credentials",
        help="Provide application credentials file path")

    #subparser for scritps
    #dest used to determined which command user selected: ARGS.command
    subparsers = parser.add_subparsers(title = "gtracks subcommands",
                dest ="command")

    #parsers for each script
    #makeHub
    makeHub_parser = subparsers.add_parser("makeHubDb")
    makeHub_parser.add_argument("hubDbname",help="Enter hubDb Spreadsheet Name")

    #addHub
    addHub_parser = subparsers.add_parser("addHub")
    addHub_parser.add_argument("hubName", help="Enter hubName")

    ARGS = parser.parse_args()
    #print "ARGS.command = %s" % ARGS.command


#find an optional -c argument and returns it
def getCredentialsArg():
    global APPLICATION_CREDENTIALS
    #-c provided and valid
    if ARGS.c is not None and os.path.isfile(os.path.abspath(ARGS.c)):
        APPLICATION_CREDENTIALS = os.path.abspath(ARGS.c)
    #leave APPLICATION_CREDENTIALS as None
    else:
        return

#call the appropriate script
def selectScript(AUTH_GSPREAD_OBJ):
    global AVAILABLE_SCRIPTS, ARGS

    #build function name
    function_str = ARGS.command + "." + ARGS.command + "Main" +\
        "(AUTH_GSPREAD_OBJ, ARGS)"

    print "function_str = %s" % function_str

    #call the function
    eval(function_str)
    exit()


if __name__ == "__main__":
    main()
