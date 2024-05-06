# Project Description

This project involves extracting data from a PostgreSQL instance using Python, performing data cleaning locally, uploading the cleaned data back to the SQL instance, creating a local CRUD (Create, Read, Update, Delete) system for the instance, and implementing a special function for the CRUD that utilizes the GPT API to understand user intent and execute actions in the database.

## Tasks Overview

1. Extract Data from PostgreSQL: Use Python to extract data from a PostgreSQL database.
2. Clean Data Locally: Review data types, inconsistencies, and missing values locally.
3. Upload Cleaned Data: Upload the cleaned data back to the PostgreSQL instance.
4. Create Local CRUD: Implement a CRUD system locally for the PostgreSQL instance.
5. Special Function Using GPT API: Develop a function that utilizes the GPT API to analyze user input and perform corresponding actions in the database.
6. Transfer CRUD to FastAPI: Transition the complete CRUD system to an API using FastAPI, utilizing appropriate API methods such as GET, POST, DELETE, and PUT.

## Project Structure

- README.md: This document provides an overview of the project and its tasks.
- requirements.txt: Includes all dependencies needed for the project.
- main.py: Contains the main code for the project.
- database 
    - models.py: Contains the Classes used in the project, to import them into the files that need them.
    - database.py: This file is in charge of downloading the DataBase from the PostgreSQL instance and using pandas to transform it into a DataSet for processing.
    - cleaning_data.py: The code in this file is responsible for cleaning the data after downloading it from the PostgreSQL instance.
    - crud.py: This code is the one in charge of the functions of the crud and the function of gpt.

## Usage Instructions

1. Setup Environment: Ensure Python and the required dependencies from requirements.txt are installed, for install the dependencies use "pip install -r requirements.txt".
2. For running main.py first create a file .env with the API key of openai, it is exported as OPENAI_API_KEY variable.
3. Run main.py: Execute main.py to initiate the project, use "uvicorn main:app --reload" to initiate the project.
4. Enter the localHost to begin working with the database and the functions of the CRUD, use the URL: "http://127.0.0.1:8000/docs" or access the endpoints.
5. The FastAPI interface will request information about the database in order to carry out any of the requests.
6. To delete, the API will ask for the id in order to delete the row with that id. 
7. For using the GPT function, introduce the prompt you want to use. For better understanding, it's recommended to use the words "create", "read", "update", or "delete".