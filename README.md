# Description

This project's objective is to integrate web forms on your website with Google Sheets within your Google Drive account. This integration facilitates a user-friendly approach to managing received data compared to traditional database querying methods. 
By automatically populating form submissions into a Google Sheet, it offers the possibility for **non-technical people to manage the acquired data**

# Quickstart setup  
### Serverless
Required to deploy our application to the cloud platform of our choice, in this case, its helping us to deploy the project inside AWS.
- **Serverless framework**: `sudo npm i -g serverless`
- serverless config credentials --provider aws --key YOUR_KEY --secret YOUR_SECRET (if you dont have your cred Keys go to [Google Cloud and AWS credentials](google-cloud-and-aws-credentials)
- More complete instalation Tutorial: https://www.serverless.com/framework/docs/getting-started

### **Google Cloud and AWS Credentials**
Google Cloud credentials are required to populate the credentials.json file, enabling Google API usage. AWS credentials are necessary for the serverless-cli to obtain all the required permissions to deploy the infrastructure to your AWS account.
- **Google API Credentials**: just go to [this page](https://developers.google.com/drive/api/quickstart/python?hl=pt_BR) -> Enable API -> select your project and follow the steps
- **AWS credentials**:
  - Put these commands on your terminal: `sudo apt install awscli` then `aws configure`
  - Go to *AWS IAM console* -> *Security credentials* -> *Access keys* -> Create access key -> store the keys on the file opened by the `aws configure` command
### Python
The project was coded using python language so it's necessary to have **Python** and its dependency manager **PIP** installed on your machine.
- **Python**: https://pip.pypa.io/en/stable/installation/
- **PIP**: https://pip.pypa.io/en/stable/installation/
- **How to Create a Virtual Environment?**
For Python-based services, it's recommended to create a virtual environment for isolated dependency installation.
    ```bash
    > pip install virtualenv
    > virtualenv environment_name
    > source environment_name/bin/activate
    # Use the **deactivate** command to exit the venv
    ```
----
## Useful commands:
* `sls deploy` - to deploy your application to your cloud account
* `sls logs`- to see the recently logs of the lambda
* `serverless deploy function -f functionName` - to deploy only the changes on your function (more efficient when u didnt change the infraestructure)
