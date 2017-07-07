
""" utility.py:
    Contains Common Functions:
    -require authorized gspread object (AUTH_GSPREAD_OBJ from cred.authorizeGS)
"""
#TODO: organize!
#TODO: make insertRow simpler
#TODO: checkHubDbExists make it re-use doesSheetExist


import gspread

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
    #check if it exists
    if not doesSheetExist(AUTH_GSPREAD_OBJ, name):
        #create it
        SPREADSHEET = AUTH_GSPREAD_OBJ.create(name)
        return SPREADSHEET
    else:
        print \
        "Error: Spreadsheet '%s' already exists\n\
        Please erase from Google Drive" % name
        exit()



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
        print "checkHubDbExists = %s" % HUBDB_ID
    except:
        print \
        "Error: Unable to open .hubDbId\n\
        please run makeHubDb first!"
        exit()

    #open hubDB
    if doesSheetExist(AUTH_GSPREAD_OBJ, id=HUBDB_ID):
        #return spreadsheet
        return AUTH_GSPREAD_OBJ.open_by_key(HUBDB_ID)
    else:
        #hubDb doesn't exist so exit
        print \
        "Error: hubDb Not Found\n\
        please run makeHubDb first!"
        exit()
