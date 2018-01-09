#! /usr/bin/python
"""
    Create hubDb in the user's Google Drive.
    Insert the header row.
"""

HEADER_ROW = ["hub_name", "hubId", "hub.txt url", "user/host",
              "path to hub directory"]
FILE_SAVE = ".hubDbId"
HUBDB_NAME = "hubDb"
SHEETID = None

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
import gspread
import httplib2
from apiclient import errors
import utility as util


def makeHubDbMain(ARGS, GC, DRIVE_SERVICE):
    """
    Main function:
        1. gets credentials
        2. creates the HubDb sheet
        3. inserts a header row into HubDb sheet
        4. verifies gdrivepath
        5. moves HubDb to gdrivepath
        6. saves the hubDb into .hubDb
        7. prints url of hubDb
    """
    global SCOPES, HUBDB_NAME, HEADER_ROW

    # check that .hubDbId doesn't already exist
    try:
        f = open(FILE_SAVE, 'r')
        print("makeHubDb Error: %s already exists" % FILE_SAVE)
        read_hubdbid = f.readline().rstrip()
        util.printURL(HUBDB_NAME, read_hubdbid)
        exit()
    except IOError:
        pass


    # create the new sheet
    sh = GC.create(HUBDB_NAME)

    # insert the first row
    util.insertRow(GC, sh, 'A1', HEADER_ROW)

    # if gdrive path given
    if ARGS.p is not None:
        # get the parent
        new_parent = getIdFromGDrivePath(ARGS.p, GC, DRIVE_SERVICE)
        # move sheet to the gdrivepath
        moveSheetToPath(DRIVE_SERVICE, new_parent, sh.id)
    else:
        # leave in place and share with user account
        sh.share(ARGS.e, perm_type='user', role='owner')

    # write the id to .hubDbId
    saveHubDbSheetID(sh.id)

    # print the url
    util.printURL(HUBDB_NAME, sh.id, None)


def getIdFromGDrivePath(gdrivepath, gc, drive_service):
    """
    Verifies that the path exists and returns the ID of the last file
    in the path.
    """
    global GDRIVEPATH

    # 1. split the path
    path_lst = gdrivepath.split('/')
    if path_lst[0] == '':
        del path_lst[0]
    if path_lst[-1] == '':
        del path_lst[-1]

    # ask user to give absolute path always
    parent = 'root'
    for directory in path_lst:
        try:
            # create query string for search
            if parent == 'root':
                query = "name='{0}' and mimeType contains '{1}'".\
                        format(directory, 'folder')
            else:
                query = "'{0}' in parents and name='{1}' and mimeType contains\
                        '{2}'".format(parent, directory, 'folder')

            # perform search
            search_lst = drive_service.files().list(
                q=query).execute()


            # if search_lst empty => file doesn't exist
            if not search_lst['files']:
                print("makeHubDb Error: please create '%s'" % directory)
                exit()
            # check for duplicates in parent directory
            if  len(search_lst['files']) > 1:
                print("makeHubDb Error: two files with the same name exist")
                exit()

            # save parent for next iteration
            parent = search_lst['files'][0]['id']
        except errors.HttpError, error:
                print "HTTP error = %s" % error
                exit()



    #return id of the directory the sheet will go into
    return parent

def moveSheetToPath(drive_service, parentId, sheetId):
    """
    Move sheet from root directory to gdrivepath.
    """
    # get current parents of sheet
    file = drive_service.files().get(fileId=sheetId, fields='parents,shared')\
                        .execute()

    prev_parents = ",".join(file.get('parents'))

    prev_parents = prev_parents + ',root'
    # add new parent and remove previous parents
    file = drive_service.files().update(fileId=sheetId, addParents=parentId,
                removeParents=prev_parents, fields='id,parents').execute()


def saveHubDbSheetID(sheetId):
    """
    Write the hubDbId to .hubDbId in current directory.
    """
    with open(FILE_SAVE, 'w') as f:
        f.write(sheetId+'\n')
