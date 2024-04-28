import datetime
from sqlalchemy import DateTime
import pandas as pd
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.expression import text
from openai import OpenAI
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import json


# Downloading the table from the database in postgreSQL and transforming into a DataFrame
db_url = "postgresql://default:VbwkxX41WTuY@ep-polished-frost-a41zn8lf-pooler.us-east-1.aws.neon.tech:5432/verceldb"
engine = create_engine(db_url)
sql_query = "SELECT * FROM survey"
df = pd.read_sql(sql_query, engine)

# Analyzing the columns in oder to determine if is important to delete the rows with missing values
df = df.dropna(subset=["industry","city","gender","race","job_title","education_level"])

# annual_salary has values that has a different format, in this case deleting the ","
df.loc[:, "annual_salary"] = df["annual_salary"].str.replace(",","")

# As the DataBase is taking into account only information from works, the annual_salary couldn´t be less than 1000 dolars a year, so deleting the rows that has this values on annual_salary
df = df[~df["annual_salary"].isin(["0","00","1","100"])]

# Deleting the spaces at the end of all the columns from the DataFrame
df = df.apply(lambda x: x.str.strip() if x.dtype=="object" else x)

# Converting the column annual_salary into float
df.loc[:,"annual_salary"] = df["annual_salary"].astype("float")

# Converting all the column country to lowercase
df["country"] = df["country"].str.lower()

# Checking the column country from the DataFrame and converting the different forms the people from the survey answer into unique format
df["country"] = df["country"].replace({"usa": "united states", "us": "united states", "u.s.": "united states","united states of america": "united states", "u.s.a.": "united states","u.s": "united states","america": "united states", "united state": "united states", "unites states": "united states", "united stated": "united states", "u.s.a": "united states", "u. s.": "united states", "united sates": "united states", "the united states": "united states", "united state of america": "united states", "🇺🇸": "united states", " unitedstates": "united states"})
df["country"] = df["country"].replace({"uk": "united kingdom","england": "united kingdom","u.k.":"united kingdom", "england, uk": "united kingdom", "wales": "united kingdom", "scotland": "united kingdom", "england, united kingdom": "united kingdom"})
df["country"] = df["country"].replace({"the netherlands": "netherlands"})
df["country"] = df["country"].replace({"nz": "new zealand"})

# Deleting any row that has less than 5 equal names, after checking the main rows from the DF
value_count_country = df["country"].value_counts()
no_values_country = value_count_country[value_count_country >= 5].index
df = df[df["country"].isin(no_values_country)]

# Converting all the column city to lowercase
df.loc[:,"city"] = df["city"].str.lower()

# Checking the column city from the DataFrame and converting the different forms the people from the survey answer into unique format
df.loc[:,"city"] = df["city"].replace({"new york city": "new york", "nyc": "new york"})
df.loc[:,"city"] = df["city"].replace({"washington, dc": "washington", "washington dc": "washington", "dc": "washington"})

# Deleting any row that has less than 5 equal names, after checking the main rows from the DF
value_count_city = df["city"].value_counts()
no_values_city = value_count_city[value_count_city >= 5].index
df = df[df["city"].isin(no_values_city)]

# Converting the df_final_state into df_final, that is going to be the last df.
df_final = df

# Creating a column in order to have a count for each row, as an id
df_final = df_final.assign(id=range(1, len(df_final) + 1))

# uploading the clean DataFrame into the instance SQL transforming it into a sql document.
df_final.to_sql("final_data_andres", con=engine, if_exists="replace")


db_url = "postgresql://default:VbwkxX41WTuY@ep-polished-frost-a41zn8lf-pooler.us-east-1.aws.neon.tech:5432/verceldb"
engine = create_engine(db_url)
sql_query = "SELECT * FROM final_data_andres"
df_final1 = pd.read_sql(sql_query, engine)
Base = declarative_base()


# Creating a Class in order to identify the type of data in each Column
class Datos(Base):
    __tablename__ = "final_data_andres"
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
    years_experience_overall = Column(String)
    years_experience_field = Column(String)
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
        query = text("SELECT * FROM final_data_andres")
        return session.execute(query).fetchall()
        # return session.query(text("final_data_andres")).all()

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


# CRUD.create({"id": 22610, "age": "18-25", "industry": "construction", "job_title": "python", "job_context": "python", "annual_salary": 10000, "additional_compensation": "None", "currency": "USD", "income_context": "None", "country": "united states", "us_state": "florida", "city": "miami", "years_experience_overall": "18-25", "years_experience_field": "18-25", "education_level": "college", "gender": "Man", "race": "Black"})

# CRUD.update_data(22610, {"id": 22610, "age": "18-25", "industry": "production", "job_title": "python", "job_context": "python", "annual_salary": 10000, "additional_compensation": "None", "currency": "USD", "income_context": "None", "country": "united states", "us_state": "florida", "city": "miami", "years_experience_overall": "18-25", "years_experience_field": "18-25", "education_level": "college", "gender": "Man", "race": "Black"})

# CRUD.delete_data(22610)

rows = CRUD.read()

print(df_final1.columns)
if rows:
    last_row = rows[-1]
    print(last_row)
else:
    print("No data found")

# Using the api key and creating an instance for a class
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


# Creating a function to process the answer generated by the OpenAI API, the answer will be in json format and depending on the respones it would active a difFerent function (create,read,update,delete)
def process_gpt_response(response):
    intent = response["choices"][0]["message"]["content"]

    if intent.startswith("create"):
        CRUD.create(intent.split(":")[1])
        return {"message": "Data created successfully."}
    elif intent.startswith("read"):
        return CRUD.read()
    elif intent.startswith("update"):
        CRUD.update_data(intent.split(":")[1])
        return {"message": "Data updated successfully."}
    elif intent.startswith("delete"):
        CRUD.delete_data(intent.split(":")[1])
        return {"message": "Data deleted successfully."}
    else:
        return {"error": "Invalid intent."}


response_json = {
    "choices": [
        {
            "message": {
                "content": "read dataframe plis",
            }
        }
    ]
}

mensaje = response_json["choices"][0]["message"]["content"]
partes = mensaje.split(" : ")
datos_nueva_fila = {}

# create a row in the dataframe taking into account that is a :38 years old man that works in the industry of construction the job title is architech, has an annual salary of 10000 USD a year, lives in the united states in miami florida, has 17 years of experience overall and in the field has 18 years of experience, has a college degree is a white person and is a man and create it with the id 22610!

for parte in partes[1:]:
    columna, valor = parte.split(" is ")
    datos_nueva_fila[columna.strip()] = valor.strip()

if "id" in datos_nueva_fila:
    datos_nueva_fila["id"] = int(datos_nueva_fila["id"])
else:
    datos_nueva_fila["id"] = None

if "annual_salary" in datos_nueva_fila:
    datos_nueva_fila["annual_salary"] = float(datos_nueva_fila["annual_salary"])
else:
    datos_nueva_fila["annual_salary"] = None

CRUD.create(datos_nueva_fila)

rows = CRUD.read()

#print(df_final1.columns)
#if rows:
    #last_row = rows[-1]
    #print(last_row)
#else:
    #print("No data found")


print(process_gpt_response(response_json))

# app = FastAPI()


# defining a class using pydantic each attribute represent a data field and has the type.
# class DataItems(BaseModel):
    #id: int
    #timestamp: datetime.time
    #age: str
    #industry: str
    #job_title: str
    #job_context: str
    #annual_salary: float
    #additional_compensation: str
    #currency: str
    #currency_other: str
    #income_context: str
    #country: str
    #us_state: str
    #city: str
    #years_experiences_overall: str
    #years_experiences_field: str
    #education_level: str
    #gender: str
    #race: str


# Set up a route POST that allows to create new elements in the DataBase and give back the data of the created elements with the estructure of the DataItems
#@app.post("/items/", response_model=DataItems)
#def create_item_route(item_data: DataItems, db: Session = Depends(get_db)):
    #return CRUD.create(db, item_data)


# Set up a route GET that show all the DataBase
#@app.get("/items/", response_model=list[DataItems])
#def read_items(db: Session = Depends(get_db)):
    #return CRUD.read(db)


# Set up a route PUT in order to update a row from the DataBase, using the id in order to know which row it has to be update and using a dictionary to complete the information
#@app.put("/items/{item_id}", response_model=DataItems)
#def update_item(item_id: int, item_data: DataItems, db: Session = Depends(get_db)):
    #return CRUD.update_data(db, item_id, item_data)


# Set up a route DELETE in order to delete a row from the project.
#@app.delete("/items/{item_id}", response_model=DataItems)
#def delete_item(item_id: int, db: Session = Depends(get_db)):
    #return CRUD.delete_data(db, item_id)


