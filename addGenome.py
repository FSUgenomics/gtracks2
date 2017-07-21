
""" addGenome.py:

"""

GENOME_SH_FIELDS = ["genome", "trackDb", "_trackDbId", "twoBitPath", "organism",
    "defaultPos", "scientificName"]

def addGenomeMain(AUTH_GSPREAD_OBJ, ARGS):
    print "ARGS = %s" % ARGS

    #open _hubDb
    hubDb = util.openHubDb(AUTH_GSPREAD_OBJ, FILE_SAVE)

    #find ARGS.hubName row index


    #get hubId and open hub!


    #create new spreadsheet called hubName_genomes and place id in _genomesId of hubName_hub
