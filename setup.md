[Back to README.md](https://github.com/dvera/gtracks2)  

### Setup:  
---   
To get started using `gtracks`, you will need to complete three steps:  
 1. Create a Google Service Account.  
 2. Enable Google Drive API and Google Sheets API on the account.  
 3. Create and share a parent directory in your Google Drive with the service account.  

A similar tutorial can be found [here](https://github.com/juampynr/google-spreadsheet-reader). 

#### Tutorial:  
##### Google Service Account  
---  
To setup a Google Service Account, go [here](https://console.developers.google.com/flows/enableapi?apiid=drive).  

 ![Creating Account](https://github.com/dvera/gtracks2/blob/master/imgs/service_account1.png)  
 
 Click on create project.  
 
  ![Creating Account2](https://github.com/dvera/gtracks2/blob/master/imgs/service_account2.png)  
  
 After creating a project, click on "Go to credentials".  
 
  ![Creating Account3](https://github.com/dvera/gtracks2/blob/master/imgs/service_account3.png)  
 
 Next, please be sure to select the following options:  
 
  ![Creating Account4](https://github.com/dvera/gtracks2/blob/master/imgs/service_account4.png)  
 
 Selecting these options will allow using `gtracks` without signing in to your Google account each time.   
 At the next screen, choose the following options:  
 
 ![Creating Account5](https://github.com/dvera/gtracks2/blob/master/imgs/service_account5.png)   
 
 **The previous step will trigger the downloading of your key. Please rename the key "demo_service_account.json", and place it `gtracks`' working directory.**    
 
  ![Creating Account6](https://github.com/dvera/gtracks2/blob/master/imgs/service_account6.png)  
 
 ![Creating Account7](https://github.com/dvera/gtracks2/blob/master/imgs/service_account7.png)  
 
 #### Enable Google Drive API and Google Sheets API  
 ---  
 Give the Service Account permissions to use the Drive API and Sheets API.  
 Otherwise, it will not be able to locate files in your Google Drive nor will it be able to create sheets.  

  Start by clicking on the top left corner and select "API and Services".  
  
 ![Enabling Drive API1](https://github.com/dvera/gtracks2/blob/master/imgs/enable1.png) 
 
 When the menu expands, click on "Dashboard".  
 
 ![Enabling Drive API2](https://github.com/dvera/gtracks2/blob/master/imgs/enable2.png) 
 
 Click on "Enable APIs and Services".  
 
 ![Enabling Drive API3](https://github.com/dvera/gtracks2/blob/master/imgs/enable3.png)  
 
 Type "Drive" or "Google Drive" to find the Google Drive API.  
 
 ![Enabling Drive API4](https://github.com/dvera/gtracks2/blob/master/imgs/enable4.png)  
 
 When it is enable, it will look like the following:  
 
 ![Enabling Drive API5](https://github.com/dvera/gtracks2/blob/master/imgs/enable5.png)  
 
 **Repeat the steps to enable the Google Sheets API.***  
  
 #### Create and share a parent directory in your Google Drive  
 ---  
 Create a 'parent' directory and share it with the Service Account.  
 Sharing the directory will allow the Service Account to create files in your Google Drive.   
 
 First, create a new folder in your Google Drive.  
 
 ![Share Folder](https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder1.png)  
 
 Next, share it with the Service Account.  
 
 ![Share Folder2](https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder2.png)  
 
 To share the the directory with the Service Account, you will need the Service Account's email.  
 Get the Service Account email by clicking on the top left menu selecting "IAM & admin".  
 With the project selected, you will see the Service Account email.  
 
 ![Share Folder3](https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder3.png)  
 
 Copy and paste the service account into the "Share with others" field.  
 
 ![Share Folder4](https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder4.png)  
 
 ** gtracks will only modify files within this parent directory ** (unless another directory has been shared with it).  
 
 #### Summary:  
 ---  
 We created a Google Service Account.  
 We enable Google Drive and Sheets API on the account.  
 We created a 'parent' directoy in your Google Drive.  
 We shared that directory with your Service Account.  
 
 Now, you can start using `gtracks`.  
 
 [Back to README.md](https://github.com/dvera/gtracks2)
