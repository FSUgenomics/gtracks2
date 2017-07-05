
""" credentials.py:
    Requires path to Application Credentials JSON File or will use default
    Returns Authorized gspread object:
    1. Gets credentials (getCredentials)
    2. Returns authorized gspread object (authorizeGS)
    Alternatively,
    3. Returns service object (getServiceObj)
    Service Object is used directly with the Google API
"""

#TODO: test the functions
#TODO: add scope for writing and reading sheets!


import os                                #checks path
import webbrowser                        #opens tab
from oauth2client.file import Storage    #gets/puts credentials
from oauth2client import client          #flow object to get creds
from googleapiclient import discovery    #builds service object
import gspread                           #for authorized gspread obj

################################
########GLOBAL VARIABLES
################################
#file that will hold access and refresh token
TOKEN_FILE = "token_file"

#flow parameters
#filename containing applications credential
APPLICATION_CREDENTIALS = "gtracks_application_credentials.json"
SCOPE = 'https://www.googleapis.com/auth/drive'
URI = 'urn:ietf:wg:oauth:2.0:oob'

#discovery.build service parameters
SERVICE = "sheets"
VERSION = "v4"

AUTH_CODE = None
#objects
FLOW = None
CREDENTIALS = None
#alt return service obj
SERVICE_OBJ = None


######################
##PUBLIC INTERFACE
######################

#creates and returns authorized gspread object
def authorizeGS(cred_path):
    global CREDENTIALS
    CREDENTIALS = getCredentials(cred_path)

    #returns authorized gspread object
    gc = gspread.authorize(CREDENTIALS)

    return gc


#gets and returns credentials object
def getCredentials(cred_path):
    global AUTH_CODE, FLOW, CREDENTIALS, TOKEN_FILE

    checkAppCredentials(cred_path)

    #object for storing and retrieving credentials
    storage = Storage(TOKEN_FILE)

    #create flow object that helps acquire credentials
    FLOW = createFlowObject()

    #do we already have the tokens?
    if not os.path.isfile(os.path.join(os.getcwd(),TOKEN_FILE)):
        AUTH_CODE = getAuthCode()

        #swap auth_code for credentials
        CREDENTIALS = FLOW.step2_exchange(AUTH_CODE)

        #storage object writes them to the TOKEN_FILE
        storage.put(CREDENTIALS)
    #already exist, so retrieve
    else:
        CREDENTIALS = storage.get()

    #REVIEW: check credentials (if not credentials or credentials.invalid?)

    return CREDENTIALS


###ALTERNATIVE RETURN SERVICE OBJECT
#in case need to use google api directly instead of gspread
def getServiceObj():
    global CREDENTIALS, SERVICE, VERSION, SERVICE_OBJ
    #credentials to authorize requests
    http_auth = CREDENTIALS.authorize(httplib2.Http())

    #return
    SERVICE_OBJ = discovery.build(SERVICE, VERSION, http_auth)
    return SERVICE_OBJ


######################
##PRIVATE INTERFACE
######################

#check that a path to app credentials exists
def checkAppCredentials(cred_path):
    global APPLICATION_CREDENTIALS

    #1. check cred path arg and exists
    if cred_path is not None and os.path.isfile(os.path.abspath(cred_path)):
        #make cred_path absolute
        APPLICATION_CREDENTIALS = os.path.abspath(cred_path)
        return

        #2. else use default if it exists
    elif os.path.isfile(os.path.join(os.getcwd(), APPLICATION_CREDENTIALS)):
        return

        #else print error
    else:
        print \
        "Error: No Application Credentials Provided.\n\
        Please find or create a credentials file \n\
        and save it in this directory %s\n\
        or use '-c' flag to specify a path to it" % APPLICATION_CREDENTIALS
        exit()

#flow object helps acquire credentials to authorize gtracks
def createFlowObject():
    #creates flow object
    flow = client.flow_from_clientsecrets(
        APPLICATION_CREDENTIALS, scope = SCOPE,
        redirect_uri = URI)

    #REVIEW: not needed
    flow.params['access_type'] = 'offline'

    return flow


#open tab and read authentication code
def getAuthCode():
    global FLOW
    #url to give permission and get auth code
    auth_uri = FLOW.step1_get_authorize_url()

    #open browser tab
    webbrowser.open(auth_uri)

    #get authentication code from user
    return raw_input('Enter the auth code: ')
