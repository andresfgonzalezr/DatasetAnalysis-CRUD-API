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
- database: 
    - models.py: Contains the Class from the schemas of the database that is used in the CRUD.
    - database.py: This file is in charge of downloading the DataBase from the PostgreSQL instance and using pandas to transform it into a DataSet for processing.
    - cleaning_data.py: The code in this file is responsible for cleaning the data after downloading it from the PostgreSQL instance.
    - crud.py: This code is the one in charge of the functions of the crud and the function of gpt.
- utils:
    - models.py: In this file is the request model from the API used to run main.py.

## Usage Instructions

1. Setup Environment: Ensure Python and the required dependencies from requirements.txt are installed, for install the dependencies use "pip install -r requirements.txt".
2. For running main.py first create a file .env with the API key of openai and the URL of the database, it is exported as OPENAI_API_KEY variable and DATABASE_URL variable.
  - For the API key it can be downloaded from the OpenAI Overview page, log in with your email address, go to settings, click on "Your Profile" and go to the User API keys.
  - For the URL of the database you can create the variable using vercel.
3. Run main.py: Execute main.py to initiate the project, use "uvicorn main:app --reload" to initiate the project.
4. Enter the localHost to begin working with the database and the functions of the CRUD, use the URL: "http://127.0.0.1:8000/docs" or access the endpoints.
5. The FastAPI interface will request information about the database in order to carry out any of the requests.
6. To use the GPT function, input the desired prompt. It's best to specify the database request type in the prompt. For reading and updating, include relevant information (e.g., age, location, salary). For reading and deleting, provide the row ID and specify the action (create, read, update, or delete).