from sqlalchemy.sql.expression import text
from models import Datos, Session, session
import json
from database import client
from typing import Annotated
from fastapi import Depends


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

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
    def read_by_id(data_id):
        query = text("SELECT * FROM final_data_andres WHERE id= :data_id")
        result = session.execute(query, {"data_id": data_id}).fetchall()
        return result

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


def get_gpt(input_prompt):
    user_prompt = (f'''
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
        the prompt I have is this one: {input_prompt}
        if in the prompt any of the fields has no information give it to me with None, this info is going to be used in a python DF
        also identify and show me if the prompt is create, update, read or delete, create 2 dictionaries the first one with the action and the second one with the data
                   ''')

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
        CRUD.create(data_dictionary)
    elif data_response["action"] == "read":
        CRUD.read_by_id( )
    elif data_response["action"] == "update":
        CRUD.update_data(data_id_gpt, data_dictionary)
    elif data_response["action"] == "delete":
        CRUD.delete_data(data_id_gpt)

    print(mesage_response)
    print(data_dictionary)
    print(data_id_gpt)


print(get_gpt("read row  with the id 1"))