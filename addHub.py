
""" addHub.py:
    Once makeHubDb has been called,
    addHub is used to create a hub, add hubs to _hubDb spreadsheet, and to
    write the corresponding hub.txt.

    Sample call:
    python gtracks.py addHub [hub_name] <-s shortLabel> <-l longLabel> <-g genomesFile>
    <-e email> <-u url of hub on server>
"""

import credentials as cred
import utility as util
import gspread
import os           #for $USER, $HOSTNAME
import shutil


FILE_SAVE = ".hubDbId"
HUB_FIELDS = ["hub", "shortLabel", "longLabel", "genomesFile",
                "email", "descriptionUrl", "_genomesId"]

NEW_HUB_ID = None
HUB_DIR_PATH = None

#main function: creates hub, adds row to hubDb and writes hub to file
def addHubMain(AUTH_GSPREAD_OBJ, ARGS):
    global FILE_SAVE, HUB_FIELDS, NEW_HUB_ID, HUB_DIR_PATH

    #####HUBDB: check hubDb exists (both .hubDbId file and online spsheet)
    hubDb = util.openHubDb(AUTH_GSPREAD_OBJ, FILE_SAVE)

    #error checking:
    #A. check not overwriting directory
    errorMssg = ""
    HUB_DIR_PATH = os.path.join(os.getcwd(), ARGS.hubName)
    if os.path.exists(HUB_DIR_PATH):
        errorMssg = "addHub Error: " + HUB_DIR_PATH + " already exists!"

    #B. check not replacing entry in hubDb
    #index of column containing hub_name values
    ind = hubDb.sheet1.row_values(1).index("hub_name") + 1
    #find empty row
    first_empty_row = hubDb.sheet1.col_values(ind).index("")
    #get hub_name column
    hubName_col =\
     hubDb.sheet1.col_values(ind)[:first_empty_row]

    print "hubName ind = %s col = %s" % (ind, hubName_col)

    #error if hub_name entry already exists in hubDb
    if ARGS.hubName in hubName_col:
        errorMssg  +=\
        "\naddHub Error: Replacing hub '%s' in hubDb '%s'" %\
        (ARGS.hubName, hubDb.title)
        #empty_row_num = hubName_col.index(ARGS.hubName) + 1

    if errorMssg != "":
        print errorMssg
        exit()

    #####HUB: create with fields and insert row
    #1. create new Hub spreadsheet with fields (exits if error)
    #we want to create another one even if it's already there!
    spsheet = util.createSheet(AUTH_GSPREAD_OBJ, ARGS.hubName + "_hub")

    #2. save its id
    NEW_HUB_ID = spsheet.id

    #3. populate the Hub spreadsheet fields and arguments
    #insert fields in first column
    util.insertRow(AUTH_GSPREAD_OBJ, spsheet, "A1", HUB_FIELDS)

    hubRow = createHubRow(ARGS)
    util.insertRow(AUTH_GSPREAD_OBJ, spsheet, "A2", hubRow)

    #####HUBDB: write row
    #5
    #pass them to insert row!
    startcell = "A" + str(first_empty_row)

    #create the row
    hubDbRow = createHubDbRow(ARGS)

    #insert it
    util.insertRow(AUTH_GSPREAD_OBJ, hubDb, startcell, hubDbRow)

    #####HUB: write the hub into a file
    #create a directory
    createHubDirectory(ARGS.hubName)

    #write hubFile
    util.writeFile(HUB_DIR_PATH, "hub.txt", spsheet)

    #print the URL
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

    print "createHubDirectory HUB_DIR_PATH = %s" % HUB_DIR_PATH
    if not os.path.exists(HUB_DIR_PATH):
        os.makedirs(HUB_DIR_PATH)
    else:
        #do not remove directory, it contains user data
        print "\
        addHub Error: directory '%s' already exists.\n\
        Overwriting '%s' file only" % HUB_DIR_PATH
