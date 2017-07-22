
""" addGenome.py:

"""

#TODO: check that need all of these!
import utility as util
import os           #for $USER, $HOSTNAME

FILE_SAVE = ".hubDbId"
GENOME_SH_FIELDS = ["genome", "trackDb", "_trackDbId", "twoBitPath", "organism",
    "defaultPos", "scientificName"]

def addGenomeMain(AUTH_GSPREAD_OBJ, ARGS):
    global FILE_SAVE

    #open _hubDb
    hubDb = util.openHubDb(AUTH_GSPREAD_OBJ, FILE_SAVE)

    #find corresponding hub and its sheetid

    #find ARGS.hubName row index
    col_ind_hub = hubDb.sheet1.row_values(1).index("hub_name") + 1
    row_ind_for_hub = hubDb.sheet1.col_values(col_ind_hub).index(ARGS.hubName) + 1

    #TODO: error check if corresponding hub not found?????!!*****
    #get hubId and open hub!
    col_ind_hubId = hubDb.sheet1.row_values(1).index("hubId") + 1
    hubDb_row = hubDb.sheet1.row_values(row_ind_for_hub)


    #open the hub
    hub_SH = util.openSPheet(AUTH_GSPREAD_OBJ, hubDb_row[col_ind_hubId-1])


    #in hub, find the genomesId value
    col_genomesId_ind = hub_SH.sheet1.row_values(1).index("_genomesId")
    hub_row = hub_SH.sheet1.row_values(2)


    ####genomesId == ""
    if hub_row[col_genomesId_ind] == "":
        #create new spreadsheet ${hubName}_genomes
        genomes_SH = util.createSheet(AUTH_GSPREAD_OBJ, ARGS.hubName+"_genomes")

        #place sheet id in ${hubName}_hub under _genomesId
        hub_SH.sheet1.update_cell(2,col_genomesId_ind+1, genomes_SH.id)

        #insert field row onto $hubName_genomes
        util.insertRow(AUTH_GSPREAD_OBJ, genomes_SH, "A1", GENOME_SH_FIELDS)

        #insert provided values!!
        lst = createGenRow(ARGS)
        util.insertRow(AUTH_GSPREAD_OBJ, genomes_SH, "A2", lst)

        #create ${hubName}_trackDb
        track_Db = util.createSheet(AUTH_GSPREAD_OBJ, ARGS.hubName + "_trackDb")

        #name the first sheet $genomeName
        track_Db.sheet1.update_title(ARGS.genomeName)


        #find the _trackDbId column
        col_trackDbId_ind = genomes_SH.sheet1.row_values(1).index("_trackDbId")


        #save the ${hubName}_trackDb id to the _trackDbId column of $hubName_genomes
        genomes_SH.sheet1.update_cell(2, col_trackDbId_ind+1, track_Db.id)


    ####genomesId != ""
    else:
        #TODO: test that bobo exits if genome already there
        #get _hub.genomesId
        genomes_SH_id = hub_row[col_genomesId_ind]


        #open $(hubName)_genomes using ${hubName}_hub.genomesId
        genomes_SH = util.openSPheet(AUTH_GSPREAD_OBJ, genomes_SH_id)

        #check if ${genomeName} exists in the genome column ==> exit
        #get genome column
        gen_col_ind = genomes_SH.sheet1.row_values(1).index("genome") + 1


        if ARGS.genomeName in genomes_SH.sheet1.col_values(gen_col_ind):
            #already exists so exit!
            print "\
            Error addGenome: '%s' already exists\n\
            exiting..." % ARGS.genomeName
            exit()

        #else add new row with arguments
        lst = createGenRow(ARGS)
        #find next empty row
        empty_row = genomes_SH.sheet1.col_values(1).index("")
        startCell = "A" + str(empty_row+1)


        util.insertRow(AUTH_GSPREAD_OBJ, genomes_SH, startCell, lst)

        #get trackDbId from previous entry
        trackDbId_ind = genomes_SH.sheet1.row_values(1).index("_trackDbId")
        trackDbId = genomes_SH.sheet1.col_values(trackDbId_ind+1)[empty_row-1]


        #open ${hubName}_trackDb using trackDbId var from ${hubName}_genomes
        trackDb = util.openSPheet(AUTH_GSPREAD_OBJ, trackDbId)

        #create new sheet in _trackDb called $genomeName
        trackDb.add_worksheet(ARGS.genomeName, 1000, 1000)

    #write the genomes.txt and bbi files
    #def writeFile(dir_path, filename, hubSheet, separator=" "):
    GENOME_PATH = os.path.join(os.getcwd(), ARGS.hubName)
    util.writeFile(GENOME_PATH, "genomes.txt", genomes_SH)

    #create bbi directory if it doesn't exist!
    if not os.path.exists(os.path.join(GENOME_PATH,"bbi")):
        os.makedirs(os.path.join(GENOME_PATH,"bbi"))

#creates row for Hub from arguments
def createGenRow(ARGS):
    lst = []
    #adding default arg for trackDb
    if ARGS.t is None:
        ARGS.t = os.path.join(os.getcwd(),ARGS.genomeName, "hubDb.txt")

    lst.append(ARGS.genomeName)
    #skip one for _trackDbId
    lst.append(ARGS.t)
    lst.append("")
    lst.append(ARGS.p)
    lst.append(ARGS.o)
    lst.append(ARGS.d)

    return lst
