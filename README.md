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

main.py: Contains the main code for the project.
requirements.txt: Includes all dependencies needed for the project.
README.md: This document, providing an overview of the project and its tasks.

## Usage Instructions

1. Setup Environment: Ensure Python and required dependencies from requirements.txt are installed.
2. Run main.py: Execute main.py to initiate the project.
3. Follow Task Instructions: The code follow the task instruction in order to operate and solve the task.
4. API Endpoint Access: Upon completion, access the CRUD functionality through the FastAPI endpoints.