
""" utility.py:
    Contains Common Functions:
    -require authorized gspread object (AUTH_GSPREAD_OBJ from cred.authorizeGS)
"""

#TODO: make insertRow simpler


import gspread
import os

#############################
#CREATING A NEW SPREADSHEET
#############################
#if it already exists returns true, else returns false
def doesSheetExist(AUTH_GSPREAD_OBJ ,name=None, id=None):
    #try opening it
    try:
        if id is None:
            sh = AUTH_GSPREAD_OBJ.open(name)
            return True
        else:
            sh = AUTH_GSPREAD_OBJ.open_by_key(id)
            return True
    except gspread.exceptions.SpreadsheetNotFound:
        return False


#creates and returns the sheet!
def createSheet(AUTH_GSPREAD_OBJ, name):
    #create it
    #REVIEW: allowing duplicates of hubs
    SPREADSHEET = AUTH_GSPREAD_OBJ.create(name)
    return SPREADSHEET

    #check if it exists
    # if not doesSheetExist(AUTH_GSPREAD_OBJ, name):
    # else:
    #     pass
    #     # print \
    #     # "Utility Error: Spreadsheet '%s' already exists\n\
        # in your Google Drive, creating another one..." % name
        # exit()



#############################
#INSERTING ROW
#############################
#inserts space-separated string "fields" starting at startCell ('A1')
def insertRow(AUTH_GSPREAD_OBJ, SPREADSHEET, startCell, fields):
    #create list from string fields
    if type(fields) is str:
        fields = fields.split(" ")

    #get the first sheet!
    sh = SPREADSHEET.sheet1

    #create a cell_list with the values to insert
    last_letter = chr(len(fields) - 1 + ord('A'))

    #create range string
    range_string = startCell + ":" + last_letter + startCell[1]

    #get cells to modify
    cell_list = sh.range(range_string)

    # print "cell_list = %s list_type = %s element type = %s"
    #% (cell_list, type(cell_list), type(cell_list[0]))

    #populate the cell_list
    i = 0
    for cell in cell_list:
        cell.value = fields[i]
        i = i + 1

    # print "after editing = cell_list = %s list_type = %s"
    #% (cell_list, type(cell_list))

    #insert the values
    sh.update_cells(cell_list)

#############################
#OPENING HUBDB
#############################
#check if hubDb has been created
def openHubDb(AUTH_GSPREAD_OBJ, HUBDB_ID_FILE):

    #read spreadsheetid for hubDb
    try:
        with open(HUBDB_ID_FILE, 'r') as f:
            HUBDB_ID = f.readline()
    except:
        print \
        "Utility Error: Unable to open .hubDbId\n\
        please run makeHubDb first!"
        exit()

    #open hubDB
    if doesSheetExist(AUTH_GSPREAD_OBJ, id=HUBDB_ID):
        #return spreadsheet
        return AUTH_GSPREAD_OBJ.open_by_key(HUBDB_ID)
    else:
        #hubDb doesn't exist so exit
        print \
        "Utility Error: hubDb Sheet Not Found\n\
        please (erase .hubDbId if necessary and) run makeHubDb first!"
        exit()

#similar to openHubDb
def openSPheet(AUTH_GSPREAD_OBJ, sheetId):
    #open the hub
    if doesSheetExist(AUTH_GSPREAD_OBJ, id=sheetId):
        return AUTH_GSPREAD_OBJ.open_by_key(sheetId)
    else:
        #hub doesnt' exist
        print \
        "Utility Error: %s Sheet Not Found\n\
        please run addHub/addGenome first!" % sheetId
        printURL("hub/genome", sheetId, None)
        exit()


#############################
#CREATING A TXT FILES
#############################
#write spreadsheet into corresponding directory (example guppy/hub.txt)
def writeFile(dir_path, filename, hubSheet, separator=" "):
    #find empty column index
    empty_col_num =  hubSheet.sheet1.row_values(1).index('')
    #get first and second row
    fields = hubSheet.sheet1.row_values(1)[:empty_col_num]
    values = hubSheet.sheet1.row_values(2)[:empty_col_num]

    zipped = []
    #join them
    for field,value in zip(fields, values):
        if field[0] != "_" and value != "":
            zipped.append((field,value))

    #file name and path
    file_path = os.path.join(dir_path, filename)

    #writing
    with open(file_path, 'w') as f:
        for field,value in zipped:
            f.write(field + separator + value + "\n")



#Print
def printURL(title, SHEETID, spsheet):
    if SHEETID is not None:
        url = "https://docs.google.com/spreadsheets/d/"+SHEETID
    else:
        #create url
        url = "https://docs.google.com/spreadsheets/d/"+spsheet.id

    #alternative url
    print "\
    Your Google Sheet,'%s', can be found here: \n%s" % (title,url)
