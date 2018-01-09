# gtracks  
<a id="top">
---  

### Table of Contents:  
1. [Setup](#setup)  
2. [Sample Usage](#usage)  
3. Commands Available:  
  a. [makeHubDb](#makeHubDb)  
  b. [addHub](#addHub)    


### Setup:  
---  
<a id="setup">  
Using `gtracks` requires:   

  1. Creating a Google Service Account.
  2. Sharing a Folder in your Google Drive with the Service Account.   

**Please see [Setup](setup.md/) for instructions. **    

 
## Sample Usage:  
<a id="usage"></a>
Create a Hub first: 

  `gtracks makeHubDb`  
  
   or  
  
  `./gtracks makeHubDb`   
  
   or  
  
  `python ./gtracks makeHubDb`  
  
If the `demo_service_account.json` Service Account Key is not in the current working directory:  

  `gtracks -c /path/to/demo_service_account.json makeHubDb`  

The `-c` flag must be provided immediately after `gtracks`.  
If invalid or no credentials are provided, gtracks will search for `demo_service_account.json` in the current directory.  
  
To specify a path in your Google Drive for placing the Hub spreadsheet:  

  `gtracks makeHubDb -p /Path/to/_hubDb`  

To use a path, the starting directory must be shared with the Google Service Account.  
In our example, the `Path` directory must be shared with the Google Service Account.  
  
If no path is provided, a Gmail account must be provided:  

  `gtracks makeHubDb -e myemail@gmail.com`  
  
 `gtracks` will transfer ownership of the spreadsheet from the Service Account to your account. 
 In the previous example, the Hub spreadsheet will be placed in `myemail@gmail.com`s Google Drive root directory.  
 
 
 
 
## 1. makeHubDb:  
<a id="makeHubDb"></a>  

## 2. addHub:  
<a id="addHub"></a>  


[Back to Top](#top)

