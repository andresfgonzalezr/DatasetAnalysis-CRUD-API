import datetime
from sqlalchemy import DateTime
import pandas as pd
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from openai import OpenAI
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv


# Downloading the table from the database in postgreSQL and transforming into a DataFrame
db_url = "postgresql://default:VbwkxX41WTuY@ep-polished-frost-a41zn8lf-pooler.us-east-1.aws.neon.tech:5432/verceldb"
engine = create_engine(db_url)
sql_query = "SELECT * FROM survey"
df = pd.read_sql(sql_query, engine)

# Analyzing the columns in oder to determine if is important to delete the rows with missing values
df_sin_nulos = df.dropna(subset=["industry","city","gender","race","job_title","education_level"])

# annual_salary has values that has a different format, in this case deleting the ","
df_sin_nulos.loc[:, "annual_salary"] = df_sin_nulos["annual_salary"].str.replace(",","")

# As the DataBase is taking into account only information from works, the annual_salary couldn´t be less than 1000 dolars a year, so deleting the rows that has this values on annual_salary
df_valores_atipicos = df_sin_nulos[~df_sin_nulos["annual_salary"].isin(["0","00","1","100"])]

# Deleting the spaces at the end of all the columns from the DataFrame
df_sin_espacios = df_valores_atipicos.apply(lambda x: x.str.strip() if x.dtype=="object" else x)

# Converting the column annual_salary into float
df_sin_espacios.loc[:,"annual_salary"] = df_sin_espacios["annual_salary"].astype("float")

# Converting all the column country to lowercase
df_sin_espacios["country"] = df_sin_espacios["country"].str.lower()

# Checking the column country from the DataFrame and converting the different forms the people from the survey answer into unique format
df_sin_espacios["country"] = df_sin_espacios["country"].replace({"usa": "united states", "us": "united states", "u.s.": "united states","united states of america": "united states", "u.s.a.": "united states","u.s": "united states","america": "united states", "united state": "united states", "unites states": "united states", "united stated": "united states", "u.s.a": "united states", "u. s.": "united states", "united sates": "united states", "the united states": "united states", "united state of america": "united states", "🇺🇸": "united states", " unitedstates": "united states"})
df_sin_espacios["country"] = df_sin_espacios["country"].replace({"uk": "united kingdom","england": "united kingdom","u.k.":"united kingdom", "england, uk": "united kingdom", "wales": "united kingdom", "scotland": "united kingdom", "england, united kingdom": "united kingdom"})
df_sin_espacios["country"] = df_sin_espacios["country"].replace({"the netherlands": "netherlands"})
df_sin_espacios["country"] = df_sin_espacios["country"].replace({"nz": "new zealand"})

# Deleting any row that has less than 5 equal names, after checking the main rows from the DF
value_count_country = df_sin_espacios["country"].value_counts()
no_values_country = value_count_country[value_count_country >= 5].index
df_final_country = df_sin_espacios[df_sin_espacios["country"].isin(no_values_country)]

# Converting all the column city to lowercase
df_final_country.loc[:,"city"] = df_final_country["city"].str.lower()

# Checking the column city from the DataFrame and converting the different forms the people from the survey answer into unique format
df_final_country.loc[:,"city"] = df_final_country["city"].replace({"new york city": "new york", "nyc": "new york"})
df_final_country.loc[:,"city"] = df_final_country["city"].replace({"washington, dc": "washington", "washington dc": "washington", "dc": "washington"})

# Deleting any row that has less than 5 equal names, after checking the main rows from the DF
value_count_city = df_final_country["city"].value_counts()
no_values_city = value_count_city[value_count_city >= 5].index
df_final_city = df_final_country[df_final_country["city"].isin(no_values_city)]

# Deleting any row that has less than 5 equal names, after checking the main rows from the DF
value_count_state = df_final_city["us_state"].value_counts()
no_values_state = value_count_state[value_count_state >= 5].index
df_final_state = df_final_city[df_final_city["us_state"].isin(no_values_state)]

# Converting the df_final_state into df_final, that is going to be the last df.
df_final = df_final_state

# Creating a column in order to have a count for each row, as an id
df_final = df_final.assign(id=range(1, len(df_final) + 1))

# uploading the clean DataFrame into the instance SQL transforming it into a sql document.
df_final.to_sql("final_data", con=engine, if_exists="replace")

Base = declarative_base()


# Creating a Class in order to identify the type of data in each Column
class Datos(Base):
    __tablename__ = "survey"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    age = Column(String)
    industry = Column(String)
    job_title = Column(String)
    job_context = Column(String)
    annual_salary = Column(Float)
    additional_compensation = Column(String)
    currency = Column(String)
    currency_other = Column(String)
    income_context = Column(String)
    country = Column(String)
    us_state = Column(String)
    city = Column(String)
    years_experiences_overall = Column(String)
    years_experiences_field = Column(String)
    education_level = Column(String)
    gender = Column(String)
    race = Column(String)


# Making a connection between the code and the DataBase in order to make interactions with it
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Making a connection and closing it correctly
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# Creating  class in order to make a CRUD
class CRUD:
    # The function has the parameter data, the new data comes from the class Datos, creating the new object, and then add to the db and to confirm it make a commit
    @staticmethod
    def create(data):
        new_data = Datos(**data)
        session.add(new_data)
        session.commit()


    @staticmethod
    # Making a request to show all the table
    def read():
        return session.query("survey").all()


    @staticmethod
    # Making an update from one id in the DataBase, the value data_id is the same id from the table, and the new data is the values that are going to be updated
    def update_data(data_id, new_data):
        data_to_update = session.query(Datos).filter_by(id=data_id).first()
        for key, value in new_data.items():
            setattr(data_to_update, key, value)
        session.commit()

    @staticmethod
    # Deleting one row from the DataBase with the id
    def delete_data(data_id):
        data_to_delete = session.query(Datos).filter_by(id=data_id).first()
        session.delete(data_to_delete)
        session.commit()


# Using the api key and creating an instance for a class
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


# Creating a function to proces the answer generated by the OpenAI API, the answer will be in json format and depending on the respones it would active a difFerent function (create,read,update,delete)
def process_gpt_response(response):
    intent = response["choices"][0]["message"]["content"]

    if intent.startswith("create"):
        create(intent.split(":")[1])
        return {"message": "Data created successfully."}
    elif intent.startswith("read"):
        return read()
    elif intent.startswith("update"):
        update_data(intent.split(":")[1])
        return {"message": "Data updated successfully."}
    elif intent.startswith("delete"):
        delete_data(intent.split(":")[1])
        return {"message": "Data deleted successfully."}
    else:
        return {"error": "Invalid intent."}


def create(data):
    # The function has the parameter data, the new data comes from the class Datos, creating the new object, and then add to the db and to confirm it make a commit
    new_data = Datos(**data)
    session.add(new_data)
    session.commit()


def read():
    # Making a request to show all the table
    return session.query("survey").all()


def update_data(data_id, new_data):
    # Making an update from one id in the DataBase, the value data_id is the same id from the table, and the new data is the values that are going to be updated
    data_to_update = session.query(Datos).filter_by(id=data_id).first()
    for key, value in new_data.items():
        setattr(data_to_update, key, value)
    session.commit()


def delete_data(data_id):
    # Deleting one row from the DataBase with the id
    data_to_delete = session.query(Datos).filter_by(id=data_id).first()
    session.delete(data_to_delete)
    session.commit()


app = FastAPI()


# defining a class using pydantic each attribute represent a data field and has the type.
class DataItems(BaseModel):
    id: int
    timestamp: datetime.time
    age: str
    industry: str
    job_title: str
    job_context: str
    annual_salary: float
    additional_compensation: str
    currency: str
    currency_other: str
    income_context: str
    country: str
    us_state: str
    city: str
    years_experiences_overall: str
    years_experiences_field: str
    education_level: str
    gender: str
    race: str


# Set up a route POST that allows to create new elements in the DataBase and give back the data of the created elements with the estructure of the DataItems
@app.post("/items/", response_model=DataItems)
def create_item_route(item_data: DataItems, db: Session = Depends(get_db)):
    return CRUD.create(db, item_data)


# Set up a route GET that show all the DataBase
@app.get("/items/", response_model=list[DataItems])
def read_items(db: Session = Depends(get_db)):
    return CRUD.read(db)


# Set up a route PUT in order to update a row from the DataBase, using the id in order to know which row it has to be update and using a dictionary to complete the information
@app.put("/items/{item_id}", response_model=DataItems)
def update_item(item_id: int, item_data: DataItems, db: Session = Depends(get_db)):
    return CRUD.update_data(db, item_id, item_data)


# Set up a route DELETE in order to delete a row from the project.
@app.delete("/items/{item_id}", response_model=DataItems)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return CRUD.delete_data(db, item_id)


