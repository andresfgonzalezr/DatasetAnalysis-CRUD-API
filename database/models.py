from sqlalchemy import DateTime
from sqlalchemy import Column, Float, String, Integer
from database.database_ import Base


class DataBase(Base):
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



