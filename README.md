# gtracks  
---  
#### Table of Contents:  
1. [Setup](#setup)  
2. [Sample Usage](#usage)  
### Commands Available:  
1. [makeHubDb](#makeHubDb)  
2. [addHub](#addHub)    


### Setup:  
<a id="setup"></a>
First, you will need to setup a Google Service Account. Then, enable the Google Drive API and the Google Sheets API on the Service Account. 

Second, you will need to create a parent directory in your Google Drive and save its id. Then, give share the parent directory with the Google Service Account you created earlier.  

A helpful tutorial to complete both steps can be found [here](https://github.com/juampynr/google-spreadsheet-reader"). 

To setup a Google Service Account, go [here](https://console.developers.google.com/flows/enableapi?apiid=drive).  


  
## Sample Usage:  
<a id="usage"></a>
  `python gtracks -c ~/application_cred.json makeHubDb myHub`  

If **"gtracks_application_credentials.json"** is already in the current working directory:  

  `python gtracks makeHubDb myHub`  
 
 
## 1. makeHubDb:  
<a id="makeHubDb"></a>  

## 2. addHub:  
<a id="addHub"></a>  

