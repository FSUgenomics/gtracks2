# gtracks2   
---  

Currently finding more persistent authentication.  
Fixing minor bugs.  

##Transferring Tracks:  
---  
transfer.py can be used to transfer tracks from one Google spreadsheet to another.  

First, you need to create an OAuth credentials file. Follow the instructions [here](https://developers.google.com/sheets/api/quickstart/python). Follow step 1.  
Be sure to name the application "*gtracks*", and download the file to the directory where transfer.py is located.  

Then, get the **SpreadSheetIDs** of the source and destination spreadsheets. *Figure 1* shows where to find it within the URL.  
Make sure that you have **proper privileges** to write to the destination spreadsheet.  

  [Sheet ID](./imgs/sheetID.png)

To summarize:  
  1. Create credentials file ('client_secret.json')
  2. Obtain SpreadSheetIDs  (ensure you have proper access)
  3. Get Proper Privileges (view SRC, edit DST)  
  4. Run `transfer.py src_ID dst_ID -t track1 track2 track3`  
  
`-c` flag can be used to provide the location of the credentials file, when it is not name `client_secret.json` or if  
it is located in a different directory.  
  
 
###Further Improvements:  
Need to place it in a Docker Container since it has a lot of dependencies.  
