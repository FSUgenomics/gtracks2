
import credentials as cred
import utility as util
import gspread
import os           #for $USER, $HOSTNAME
import shutil

#REVIEW: user@host?
#TODO: test functions

FILE_SAVE = ".hubDbId"
HUB_FIELDS = ["hub", "shortLabel", "longLabel", "genomesFile",
                "email", "descriptionUrl", "_genomesId"]

NEW_HUB_ID = None
HUB_DIR_PATH = None

#main function: creates hub, adds row to hubDb and writes hub to file
def addHubMain(AUTH_GSPREAD_OBJ, ARGS):
    global FILE_SAVE, HUB_FIELDS, NEW_HUB_ID, HUB_DIR_PATH

    #HUBDB: check hubDb exists (both .hubDbId file and online spsheet)
    #exits if not
    hubDb = util.openHubDb(AUTH_GSPREAD_OBJ, FILE_SAVE)

    #TODO:clean this up
    #BUG: checking if I can create two of the same hubs!
    #check no directory with hub already exists
    errorMssg = ""
    HUB_DIR_PATH = os.path.join(os.getcwd(), ARGS.hubName)
    if os.path.exists(HUB_DIR_PATH):
        errorMssg = "addHub Error: " + HUB_DIR_PATH + " already exists!\n"

    #check no entry exists in hubDb for hub
    #5. create entry for new Hub in HUBDB
    hubName_col = hubDb.sheet1.col_values(1)

    #find empty row or replace!!
    if ARGS.hubName in hubName_col:
        errorMssg  +=\
        "addHub Error: Replacing hub '%s' in hubDb '%s'" %\
        (ARGS.hubName, hubDb.title)
        empty_row_num = hubName_col.index(ARGS.hubName) + 1
    #first empty row
    else:
        empty_row_num = hubDb.sheet1.col_values(1).index('') + 1

    if errorMssg != "":
        print errorMssg
        exit()

    #HUB: create with fields and insert row
    #1. create new Hub spreadsheet with fields (exits if error)
    spsheet = util.createSheet(AUTH_GSPREAD_OBJ, ARGS.hubName + "_hub")

    #2. save its id
    NEW_HUB_ID = spsheet.id

    #3. populate the Hub spreadsheet fields and arguments
    #insert fields in first column
    util.insertRow(AUTH_GSPREAD_OBJ, spsheet, "A1", HUB_FIELDS)

    hubRow = createHubRow(ARGS)
    util.insertRow(AUTH_GSPREAD_OBJ, spsheet, "A2", hubRow)


    #HUBDB: write row
    #5
    #pass them to insert row!
    startcell = "A" + str(empty_row_num)

    #create the row
    hubDbRow = createHubDbRow(ARGS)

    #insert it
    util.insertRow(AUTH_GSPREAD_OBJ, hubDb, startcell, hubDbRow)

    #TODO: do not overwrite
    #create a directory
    createHubDirectory(ARGS.hubName)

    #write hubFile
    util.writeFile(HUB_DIR_PATH, "hub.txt", spsheet)

    util.printURL(ARGS.hubName, NEW_HUB_ID, spsheet)


#creates row for Hub from arguments
def createHubRow(ARGS):
    #default shortLabel = $hubName
    if ARGS.s is None:
        ARGS.s = ARGS.hubName
    #default longLabel = $hubName
    if ARGS.l is None:
        ARGS.l = ARGS.hubName

    lst = [ARGS.hubName, ARGS.s, ARGS.l, ARGS.g, ARGS.e, ARGS.u]
    return lst

#create an row for hub to go into hubDb
def createHubDbRow(ARGS):
    global NEW_HUB_ID
    #hub_name, hubId, hub.txt url, user/host, path to hub directory
    lst = []
    lst.append(ARGS.hubName)
    lst.append(NEW_HUB_ID)
    lst.append(ARGS.u)

    #if env var doesn't exist uses "default"
    user_hostname_str = os.getenv("USER", "default")\
     + "@" + os.getenv("HOSTNAME", "default")

    lst.append(user_hostname_str)

    path_to_hub_dir = os.path.join(os.getcwd(), ARGS.hubName)
    lst.append(path_to_hub_dir)
    return lst

#create a directory in cwd with hubName
def createHubDirectory(hubDirName):
    global HUB_DIR_PATH

    if not os.path.exists(HUB_DIR_PATH):
        os.makedirs(HUB_DIR_PATH)
    else:
        #BUG: do not remove the directory
        print "\
        **addHub Error: directory '%s' already exists.\n\
        Remove '%s' to change it**not really error**" % HUB_DIR_PATH
