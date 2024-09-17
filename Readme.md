# Customer Address Classification

## Project Overview

The objective of this assignment is to classify customer addresses into three categories: **Good**, **Medium**, and **Bad**. This classification is based on the quality and completeness of the customer address data. The project involves the following steps: data preprocessing, data enhancement, feature engineering, model training, and model evaluation. The trained model can be used to classify new customer addresses using a REST API.


## Features

- **Upload CSV File**: Users can upload a CSV file containing customer address data, which will be cleaned, preprocessed, and used to train a classification model.
- **Address Validation**: Uses geolocation to validate if the address exists and is complete.
- **Classification**: Classifies addresses as **Good**, **Medium**, or **Bad** based on address length, completeness, and geolocation validation.
- **Model Persistence**: Trained model is saved for future use, and the API allows prediction of new addresses.

## Installation

To run this project locally, you need to have **Python 3.10+** installed. Follow the instructions below to set up the environment.

### 1. Clone the repository

```bash
git clone git@github.com:Lokendraydv/shiprocket-assignment.git
```

### 2. Create a Virtual Environment

- python3 -m venv venv
- source venv/bin/activate   # For Linux/macOS
# or
- venv\Scripts\activate      # For Windows

### 3. Install Dependencies
- pip install -r requirements.txt


### 4. Run the Flask Application
- python3 server.py

### 5. Deployment
- We have deployed our code on Ec2.
Here is the public end points and their payloads:-

**prediction**
endpoint:- "3.109.58.9:5000/classify" 
payload:- 
{
    "Address": "405,aspiresoftserv",
    "City": "ahmedabad",
    "State": "gujarat",
    "Pincode": "587886"
}

**Model Training**
Model_training;- 3.109.58.9:5000/train
payload:- 
1. In Body select form-data, create one key with "file" name, select CSV file.
2. Then, In headers insdie key select "content-type" and in value it should be "multipart/form-data".