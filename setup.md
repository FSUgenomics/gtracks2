![Back to Readme](https://github.com/dvera/gtracks2)  

### Setup:  
---  

**Please see the [Setup](setup/) **.  

First, you will need to setup a Google Service Account. Then, enable the Google Drive API and the Google Sheets API on the Service Account. 

Second, you will need to create a parent directory in your Google Drive and save its id. Then, share the parent directory with the Google Service Account you created earlier.  

Another helpful tutorial to complete both steps can be found [here](https://github.com/juampynr/google-spreadsheet-reader"). 

To setup a Google Service Account, go [here](https://console.developers.google.com/flows/enableapi?apiid=drive).  

 ![Creating Account](https://github.com/dvera/gtracks2/blob/master/imgs/service_account1.png)  
 
 Click on create project.  
 
  ![Creating Account2](https://github.com/dvera/gtracks2/blob/master/imgs/service_account2.png)  
  
 After creating a project, click on "Go to credentials".  
 
  ![Creating Account3](https://github.com/dvera/gtracks2/blob/master/imgs/service_account3.png)  
 
 Next, please be sure to select the following options:  
 
  ![Creating Account4](https://github.com/dvera/gtracks2/blob/master/imgs/service_account4.png)  
 
 These options will prevent you from having to log in each time gtracks is called.  
 At the next screen, choose the following options:  
 
 ![Creating Account5](https://github.com/dvera/gtracks2/blob/master/imgs/service_account5.png)   
 
 **The previous step will trigger the downloading of your key. Please rename the key "service_key.json", and place it gtracks' working directory.**    
 
  ![Creating Account6](https://github.com/dvera/gtracks2/blob/master/imgs/service_account6.png)  
 
 ![Creating Account7](https://github.com/dvera/gtracks2/blob/master/imgs/service_account7.png)  
 
 
  Now, we need to allow the Service Account to call the Drive API. Otherwise, the Service Account will not be able to locate files  
  in the Google Drive folders.  
  
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
 
  
 Now, we need to create a parent directory, and share it with the Service Account.  
 This step is important because the Service Account we created is separate from our own Google Drive account.  
 Without sharing a folder with the Service Account, it will not be able to access files in our Drive.  
 
 First, create a new folder in your Google Drive.  
 
 ![Share Folder](https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder1.png)  
 
 Next, share it with the Service Account.  
 
 ![Share Folder2](https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder2.png)  
 
 Obtain the Service Account email by clicking on the top left menu and selecting "IAM & admin".  
 With the project selected, you will see the Service Account email.  
 
 ![Share Folder3](https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder3.png)  
 
 Copy and paste the service account into the "Share with others" field.  
 
 ![Share Folder4](https://github.com/dvera/gtracks2/blob/master/imgs/parent_folder4.png)  
 
 ** gtracks will only modify files within this parent directory ** (unless another directory has been shared with it).  
 
 
 To summarize, we created a Service Account, and enabled the Google Drive API on it. 
 Then, we created a parent directory in our Google Drive  
 and gave the Service Account permission to access and modify it.  
 Now, we can start using gtracks. The **$gDrivePath** in makeHubDb will only create and modify files within the parent directory.
