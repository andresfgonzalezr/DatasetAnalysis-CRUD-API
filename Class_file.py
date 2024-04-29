from sqlalchemy import DateTime
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.expression import text
from download_postgreSQL_DB import engine, df_final1

Base = declarative_base()


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


# Information to test the CRUD

# CRUD.create({"id": 22610, "age": "18-25", "industry": "construction", "job_title": "python", "job_context": "python", "annual_salary": 10000, "additional_compensation": "None", "currency": "USD", "income_context": "None", "country": "united states", "us_state": "florida", "city": "miami", "years_experience_overall": "18-25", "years_experience_field": "18-25", "education_level": "college", "gender": "Man", "race": "Black"})

# CRUD.update_data(22610, {"id": 22610, "age": "18-25", "industry": "production", "job_title": "python", "job_context": "python", "annual_salary": 10000, "additional_compensation": "None", "currency": "USD", "income_context": "None", "country": "united states", "us_state": "florida", "city": "miami", "years_experience_overall": "18-25", "years_experience_field": "18-25", "education_level": "college", "gender": "Man", "race": "Black"})

# CRUD.delete_data(22610)

# rows = CRUD.read()

# print(df_final1.columns)
# if rows:
    # last_row = rows[-1]
    # print(last_row)
# else:
    # print("No data found")