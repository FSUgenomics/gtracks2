
import credentials as cred
import utility as util
import gspread
import os           #for $USER, $HOSTNAME
import shutil

#REVIEW: default values used?
#REVIEW: user@host?
#REVIEW: url?
#TODO: implement writeHub ==> utility
#TODO: test functions
#TODO: CLEAN UP!!
#TODO: create new directory in present folder
#TODO: checked that correctly used the functions!

FILE_SAVE = ".hubDbId"
HUB_FIELDS = ["hub", "shortLabel", "longLabel", "genomesFile",
                "email", "descriptionUrl", "_genomesId"]

NEW_HUB_ID = None
HUB_DIR_PATH = None

#TODO: faster way of finding first empty cell?
def addHubMain(AUTH_GSPREAD_OBJ, ARGS):
    global FILE_SAVE, HUB_FIELDS, NEW_HUB_ID

    #HUBDB: check hubDb exists (both .hubDbId file and online spsheet)
    #exits if not
    hubDb = util.openHubDb(AUTH_GSPREAD_OBJ, FILE_SAVE)

    #HUB: create with fields and insert row
    #1. create new Hub spreadsheet with fields (exits if error)
    spsheet = util.createSheet(AUTH_GSPREAD_OBJ, ARGS.hubName)

    #2. save its id
    NEW_HUB_ID = spsheet.id

    #3. populate the Hub spreadsheet fields and arguments
    #insert fields in first column
    util.insertRow(AUTH_GSPREAD_OBJ, spsheet, "A1", HUB_FIELDS)
    #TODO: populate with arguments passed in!!
    hubRow = createHubRow(ARGS)
    util.insertRow(AUTH_GSPREAD_OBJ, spsheet, "A2", hubRow)


    #HUBDB: write row
    #5. create entry for new Hub in HUBDB

    #TODO: find empty row or replace!!

    hubName_col = hubDb.sheet1.col_values(1)
    #if already exists
    if ARGS.hubName in hubName_col:
        print \
        "addHub: Replacing hub '%s'in hubDb '%s'" % (ARGS.hubName, hubDb.title)
        empty_row_num = hubName_col.index(ARGS.hubName)+ 1
    #first empty row
    else:
        empty_row_num = hubDb.sheet1.col_values(1).index('') + 1



    #first empty row
    print "empty_row_num = %s" % empty_row_num

    #pass them to insert row!
    startcell = "A" + str(empty_row_num)

    #create the row
    hubDbRow = createHubDbRow(ARGS)

    #insert it
    util.insertRow(AUTH_GSPREAD_OBJ, hubDb, startcell, hubDbRow)

    #TODO: write hub to directory
    #create a directory
    createHubDirectory(ARGS.hubName)

    #write hubFile
    writeHub(ARGS.hubName, spsheet)


#creates row for Hub from arguments
def createHubRow(ARGS):
    #default shortLabel = $hubName
    if ARGS.s is None:
        ARGS.s = ARGS.hubName
    #default longLabel = $hubName
    if ARGS.l is None:
        ARGS.l = ARGS.hubName

    print "ARGS = %s" % ARGS
    lst = [ARGS.hubName, ARGS.s, ARGS.l, ARGS.g, ARGS.e, ARGS.u]
    print "lst = %s" % lst
    return lst

#create an row for hub to go into hubDb
def createHubDbRow(ARGS):
    global NEW_HUB_ID
    #hub_name, hubId, hub.txt url, user/host, path to hub directory
    lst = []
    lst.append(ARGS.hubName)
    lst.append(NEW_HUB_ID)
    lst.append(ARGS.u)

    #HACK: what if it doesn't exist??
    user_hostname_str = os.getenv("USER", "default")\
     + "@" + os.getenv("HOSTNAME", "default")
    #BUG: check if variable not set? use os.environ?
    lst.append(user_hostname_str)

    path_to_hub_dir = os.path.join(os.getcwd(), ARGS.hubName)
    lst.append(path_to_hub_dir)
    print "HubDbRow = %s" % lst
    return lst


#create a directory in cwd with hubName
def createHubDirectory(hubDirName):
    global HUB_DIR_PATH
    HUB_DIR_PATH = os.path.join(os.getcwd(), hubDirName)
    if not os.path.exists(HUB_DIR_PATH):
        os.makedirs(HUB_DIR_PATH)
    else:
        print "addHub: overwriting local hub at %s" % HUB_DIR_PATH
        shutil.rmtree(HUB_DIR_PATH)
        os.makedirs(HUB_DIR_PATH)

#read the spreadsheet into the directory
def writeHub(hubName, hubSheet, separator=" "):
    global HUB_DIR_PATH
    #TODO: col_values returns entire column! <== need to return only filled
    empty_row_num =  hubSheet.sheet1.col_values(1).index('')
    fields = hubSheet.sheet1.col_values(1)[:empty_row_num]
    values = hubSheet.sheet1.col_values(2)[:empty_row_num]

    #join them
    zipped = zip(fields, values)

    print "***zipped = %s" % zipped

    #file name and path
    hub_path = os.path.join(HUB_DIR_PATH, hubName)

    print "writeHub **%s**" % hub_path

    with open(hub_path, 'w') as f:
        for field,value in zipped:
            f.write(field + separator + value + "\n")

    #write
    pass
