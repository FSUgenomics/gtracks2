[Back to README.md](https://github.com/dvera/gtracks2)  

### Setup:  
---   
To get started using `gtracks`, you will need to complete three steps:  
 1. Create a Google Service Account.  
 2. Enable Google Drive API and Google Sheets API on the account.  
 3. Create and share a parent directory in your Google Drive with the service account.  

A similar tutorial can be found [here](https://github.com/juampynr/google-spreadsheet-reader). 

### Tutorial:  
##### Google Service Account  
---  
To setup a Google Service Account, go [here](https://console.developers.google.com/flows/enableapi?apiid=drive).  
 <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/service_account1.png" align="middle" height="360" width="480" alt="Creating Account">
 </p>
 
 Click on create project.  
 
  <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/service_account2.png" align="middle" height="360" width="480" alt="Creating Account2">
 </p>
  
 After creating a project, click on "Go to credentials".  
   <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/service_account3.png" align="middle" height="360" width="480" alt="Creating Account3">
  </p>
 
 Next, please be sure to select the following options:  
 
    <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/service_account4.png" align="middle" height="360" width="480" alt="Creating Account4">
  </p>
 
 Selecting these options will allow using `gtracks` without signing in to your Google account each time.   
 At the next screen, choose the following options:  
 
   <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/service_account5.png" align="middle" height="360" width="480" alt="Creating Account5">
  </p>
 
 **The previous step will trigger the downloading of your key. Please rename the key "demo_service_account.json", and place it `gtracks`' working directory.**    
  
   <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/service_account6.png" align="middle" height="360" width="480" alt="Creating Account6">
  </p>
 
  <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/service_account7.png" align="middle" height="360" width="480" alt="Creating Account7">
  </p>
 
 #### Enable Google Drive API and Google Sheets API  
 ---  
 Give the Service Account permissions to use the Drive API and Sheets API.  
 Otherwise, it will not be able to locate files in your Google Drive nor will it be able to create sheets.  

  Start by clicking on the top left corner and select "API and Services".  
  
 <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/enable1.png" align="middle" height="360" width="480" alt="Enabling Drive API1">
  </p>
 
 When the menu expands, click on "Dashboard".  

 <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/enable2.png" align="middle" height="360" width="480" alt="Enabling Drive API2">
  </p>
 
 Click on "Enable APIs and Services".  
 
  <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/enable3.png" align="middle" height="360" width="480" alt="Enabling Drive API3">
  </p>
 
 Type "Drive" or "Google Drive" to find the Google Drive API.  

  <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/enable4.png" align="middle" height="360" width="480" alt="Enabling Drive API4">
  </p>
 
 When it is enable, it will look like the following:  
 
   <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/enable5.png" align="middle" height="360" width="480" alt="Enabling Drive API5">
  </p>
 
 **Repeat these steps to enable the Google Sheets API.**
  
 ### Create and Share Parent Directory in your Google Drive  
 ---  
 Create a 'parent' directory and share it with the Service Account.  
 Sharing the directory will allow the Service Account to create files in your Google Drive.   
 
 First, create a new folder in your Google Drive.  
 
  <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder1.png" align="middle" height="360" width="480" alt="Share Folder">
  </p>
 
 Next, share it with the Service Account.  
 
 <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder2.png" align="middle" height="360" width="480" alt="Share Folder2">
  </p>
 
 To share the the directory with the Service Account, you will need the Service Account's email.  
 Get the Service Account email by clicking on the top left menu selecting "IAM & admin".  
 With the project selected, you will see the Service Account email.  
 
 <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder3.png" align="middle" height="360" width="480" alt="Share Folder3">
  </p>
 
 Copy and paste the service account into the "Share with others" field.  
 
  <p align="center">
 <img src="https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder4.png" align="middle" height="360" width="480" alt="Share Folder4">
  </p>
 
 ** gtracks will only modify files within this parent directory ** (unless another directory has been shared with it).  
 
 #### Summary:  
 ---  
 We created a Google Service Account.  
 We enable Google Drive and Sheets API on the account.  
 We created a 'parent' directoy in your Google Drive.  
 We shared that directory with your Service Account.  
 
 Now, you can start using `gtracks`.  
 
 [Back to README.md](https://github.com/dvera/gtracks2)
