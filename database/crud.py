from sqlalchemy.sql.expression import text
from database.models import Datos
from database.database import SessionLocal, session, engine
import json
from database.database import client
from sqlalchemy.orm import Session


def create(data: dict, db):
    data_dict = data
    new_data = Datos(**data_dict)
    db.add(new_data)
    db.commit()
    return new_data


# Making a request to show all the table
def read(db: Session):
    query = text("SELECT * FROM final_data_andres")
    return db.execute(query).fetchall()


def read_by_id(data_id: int, db: Session):
    query = text("SELECT * FROM final_data_andres WHERE id= :data_id")
    result = db.execute(query, {"data_id": data_id}).fetchall()
    return result


# Making an update from one id in the DataBase, the value data_id is the same id from the table, and the new data is the values that are going to be updated
def update_data(data_id: int, new_data: dict, db: Session):
    data_to_update = db.query(Datos).filter_by(id=data_id).first()
    for key, value in new_data.items():
        setattr(data_to_update, key, value)
    db.commit()
    return data_to_update


# Deleting one row from the DataBase with the id
def delete_data(data_id: int, db: Session):
    data_to_delete = db.query(Datos).filter_by(id=data_id).first()
    if data_to_delete:
        db.delete(data_to_delete)
        db.commit()
    else:
        return "id doesn´t exist"


def get_gpt(input_prompt: str, db):
    user_prompt = f'''
                   I have the next prompt, I need to extract the information about, also I have to fill out the next format and give please to me in a JSON format
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
        the prompt I have is as follows: {input_prompt}
        if any of the fields in the prompt have no information give it to me with None, this info is going to be used in a python DF
        also identify and show me if the prompt is create, update, read or delete, create two dictionaries the first one with the action and the second one with the data
                   '''

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
            temperature=0,
      messages=[
        {"role": "user", "content": user_prompt}
      ]
    )

    mesage_response = response.choices[0].message.content

    data_response = json.loads(mesage_response)
    data_dictionary = data_response["data"]
    data_id_gpt = data_dictionary["id"]

    if data_response["action"] == "create":
        create(data_dictionary, db)
        return read_by_id(data_id_gpt, db)
    elif data_response["action"] == "read":
        return read_by_id(data_id_gpt, db)
    elif data_response["action"] == "update":
        update_data(data_id_gpt, data_dictionary, db)
        return read_by_id(data_id_gpt, db)
    elif data_response["action"] == "delete":
        delete_data(data_id_gpt, db)
        return "item deleted"

# print(get_gpt("read dataframe with id 1"))
