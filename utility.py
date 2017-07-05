
""" utility.py:
    Contains Common Functions:
    -require authorized gspread object (AUTH_GSPREAD_OBJ from cred.authorizeGS)
"""
#TODO: make insertRow simpler

import gspread

#############################
#CREATING A NEW SPREADSHEET
#############################
#if it already exists returns true, else returns false
def doesSheetExist(AUTH_GSPREAD_OBJ ,name):
    #try opening it
    try:
        sh = AUTH_GSPREAD_OBJ.open(name)
        print "Error: Spreadsheet '%s' already exists %s" % (name, sh)
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
        return None


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
