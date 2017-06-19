#gtracks2   
---  

Currently finding more persistent authentication.  
Fixing minor bugs.  

#Transferring Tracks:  
---  
`transfer.py` can be used to transfer tracks from one Google spreadsheet to another.  

First, you need to create an OAuth credentials file. Follow the instructions [here](https://developers.google.com/sheets/api/quickstart/python). Follow step 1.  
Be sure to name the application "*gtracks*", create it, and download it.  
Then, rename it **"client_secret.json"** and place it in the directory containing `transfer.py`.  

The "-c" flag may be used to specify another name and location for the credentials file.  

Then, get the **SpreadSheetIDs** of the source and destination spreadsheets. *Figure 1* shows where to find it within the URL.  
Make sure that you have **proper privileges** to write to the destination spreadsheet.  

<p align="center">  

  ![Sheet ID](https://github.com/FSUgenomics/gtracks2/blob/master/imgs/sheetID.png)  
  
</p>  

To summarize:  
  1. Create credentials file ('client_secret.json')
  2. Obtain SpreadSheetIDs  
  3. Get Proper Privileges (view SRC, edit DST)  
  4. Run `transfer.py src_ID dst_ID -t track1 track2 track3`  
  
`-c` flag can be used to provide the location of the credentials file, when it is not named `client_secret.json` or if  
it is located in a different directory.   
 
###Sample Calls:  
  Simple Call:  
  `./transfer.py 1-PTkrZL9sM_Us4NHinZfldQxVCsPj6-xHQedb2lkEj0  1lDStJZQBQehfsSrI9bnOKgwa6bzzlMhoY_AXdns1SWQ -t Fam_3`  
  
  Call with Credentials:  
  `./transfer.py 1lDStJZQBQehfsSrI9bnOKgwa6bzzlMhoY_AXdns1SWQ 1-PTkrZL9sM_Us4NHinZfldQxVCsPj6-xHQedb2lkEj0 -t transcriptome_map gcPercentW50 -c ~/client_secret.json`  
  
  Call with API_Key:  
  `./transfer.py 1lDStJZQBQehfsSrI9bnOKgwa6bzzlMhoY_AXdns1SWQ 1HvIQ--bci1cWj8BY8GTtNIoik8XOsFY160aiskN6NIw -t dnsSeq_ear_macs2 cns_turcoFreeling2014 -c ../../../client_secret.json -k B1zaSyCZRo2Xq1h-APhrC7hHxFF8wyuEgT4eA7I`  
 
###Troubleshooting:  
If it fails to find the either spreadsheet, make sure to give the user proper privileges to them.  
For example, if the spreadsheets are private and owned by someone else, the script will not find them.  

If it still fails to find the spreadsheets, delete, create and download a new `client_secret.json`.  

The global variable `VALUE_OPTION` may be changed. Currently, it is set to `RAW`, so the content of the SRC track 
is copied and pasted without parsing.  Using option `USER_INPUT` will cause it to be parsed,   
which can cause problems because it may convert numbers to dates and other formats.  

Summary:  
  1. Proper Permissions  
  2. Delete `client_secret.json` and create a new one.  
  
###Important Notes:  
API_Key is not necessary. Using the API_Key does **not** allow writing to a spreadsheet even if it is public.  
Use a credentials file to allow the script to write to spreadsheets. 

If you wish to insert to another Sheet within the spreadsheet, you may carefully change the `RANGE` global variables.  

###Further Improvements:  
Need to place it in a Docker Container since it has a lot of dependencies.  
