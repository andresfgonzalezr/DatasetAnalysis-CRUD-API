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

- README.md: This document, providing an overview of the project and its tasks.
- requirements.txt: Includes all dependencies needed for the project.
- main.py: Contains the main code for the project.
- Clas_file.py: Contains the Classes used in the project, to import them into the files that need them
- database.py: This file is in charge of downloading the DataBase from the postgreSQL instance and using pandas to transform into a DataSet, to work on it.
- cleaning_data.py: The code in this file is the one that is in charge of cleaning the data after downloading the DataBase from the postgreSQL instance.

## Usage Instructions

1. Setup Environment: Ensure Python and required dependencies from requirements.txt are installed.
2. Run main.py: Execute main.py to initiate the project, use "uvicorn main:app --relod" to initiate the project.
3. Enter to the localHost to began working with the database and the functions of the crud, use the URL:"http://127.0.0.1:8000/docs" or use the endpoints.
4. The FastAPI interface will request information about the database in order to carry out any of the requests.
5. For posting the API will ask the information about the row to create.
6. For get one specific row the API will ask for the id of the row.
7. For get all the database only execute
8. For PUT introduce the information of the row you want to update.
9. For delete the API will ask for the id in order to delete the row with that id.
10. For using the GPT function, introduce the prompt you want to use, for a better understanding of the prompt is better to use the words "create", "read", "upgrade" or "delete"
11. At the end only finish the process of the API using "ctrl + c"