from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from download_postgreSQL_DB import engine, df_final1
from Class_file import Datos, Base, Session, session, CRUD


# Using the api key and creating an instance for a class
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

user_prompt = ('''
               I have the next promtp, I need to take out the information about, also I have to fill the next format and give plis to me in a json format
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
    the prompt I have is this one: create a row in the dataframe taking into account that is a :38 years old man that works in the industry of construction the job title is architech, has an annual salary of 10000 USD a year, lives in the united states in miami florida, has 17 years of experience overall and in the field has 18 years of experience, has a college degree is a white person and is a man and create it with the id 22610!
    if in the prompt any of the fields has no information give it to me with None, this info is going to be used in a python DF
    also identify and show me if the prompt is create, update, read or delete, create 2 dictionaries the first one with the action and the second one with the data
               ''')

# update a row in the dataframe taking into account that is a 28 years old man that works in the industry of construction the job title is architech, has an annual salary of 10000 USD a year, lives in the united states in miami florida, has 17 years of experience overall and in the field has 18 years of experience, has a college degree is a white person and is a man and create it with the id 22610!
# create a row in the dataframe taking into account that is a :38 years old man that works in the industry of construction the job title is architech, has an annual salary of 10000 USD a year, lives in the united states in miami florida, has 17 years of experience overall and in the field has 18 years of experience, has a college degree is a white person and is a man and create it with the id 22610!
# read dataframe with id 22610

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
        temperature=0,
  messages=[
    {"role": "user", "content": user_prompt}
  ]
)

mesage_response = response.choices[0].message.content
print(mesage_response)

data_response = json.loads(mesage_response)
data_dictionary = data_response["data"]
data_id_gpt = data_dictionary["id"]

if data_response["action"] == "create":
    CRUD.create(data_dictionary)
elif data_response["action"] == "read":
    CRUD.read_by_id(data_id_gpt)
elif data_response["action"] == "update":
    CRUD.update_data(data_id_gpt, data_dictionary)
elif data_response["action"] == "delete":
    CRUD.delete_data(data_id_gpt)

rows = CRUD.read()

if rows:
    last_row = rows[-1]
    print(last_row)
else:
    print("No data found")

print(df_final1.tail())

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


