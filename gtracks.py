
""" Main:
    1. Get Credentials (authorized gspread object)
    2. Parse Arguments
    3. Call Appropriate script (makeHubDb, addHub, etc)
    Script then Checks Arguments and Runs
"""

#TODO: add commands and subparsers!!
#BUG: -c must be provided at the very beginning for main parser to see it
#BUG: else will have to add it do each subparser?

import os
import sys
import argparse
#Local modules
import credentials as cred
import makeHubDb
import addHub
import addGenome


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
    global ARGS

    #gtracks parser
    parser = argparse.ArgumentParser(prog="gtracks")
    parser.add_argument("-c", "-credentials",
        help="Provide application credentials file path")

    #subparser for scritps
    #dest used to determined which command user selected: ARGS.command
    subparsers = parser.add_subparsers(title = "gtracks subcommands",
                dest ="command")

    #parsers for each script

    #### makeHub
    makeHub_parser = subparsers.add_parser("makeHubDb")
    #no arguments

    #### addHub
    addHub_parser = subparsers.add_parser("addHub")
    #multiple arguments, hubName is required
    #shortLabel, longLabel, genomesFile, email, url
    addHub_parser.add_argument("hubName", help="Enter hubName")
    addHub_parser.add_argument("-s", "-shortLabel", help="Enter hubName")
    addHub_parser.add_argument("-l", "-longLabel", help="Enter longlabel")
    addHub_parser.add_argument("-g", "-genomesFile", default="genomes.txt")
    addHub_parser.add_argument("-e", "-email", default="ex@example.com")
    addHub_parser.add_argument("-u", "-url", default="",
            help="Location of Hub on File Server")


    #### addHub
    addGenome_parser = subparsers.add_parser("addGenome")
    #arguments: hubName, genomeName, trackDb, twoBitPath, organism,
    #scientificName, defaultPos
    addGenome_parser.add_argument("hubName",help ="Enter corresponding hubName")
    addGenome_parser.add_argument("genomeName", help="Enter genome name")

    #TODO: help for -t, -d, -p
    addGenome_parser.add_argument("-t", "-trackDb",
        help="Enter location of hubDb.txt")
    addGenome_parser.add_argument("-p", "-twoBitPath",
        help="Enter location of hubDb.txt", default="")
    addGenome_parser.add_argument("-o", "-organism",
     help = "Enter organism name", default = "")
    addGenome_parser.add_argument("-d", "-defaultPos", default = "")

    ARGS = parser.parse_args()


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
    global ARGS

    #build function name
    function_str = ARGS.command + "." + ARGS.command + "Main" +\
        "(AUTH_GSPREAD_OBJ, ARGS)"

    #call the function
    eval(function_str)
    exit()


if __name__ == "__main__":
    main()
