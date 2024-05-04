from sqlalchemy import DateTime
from sqlalchemy import Column, Float, String, Integer
from database.database import Base
from pydantic import BaseModel
import datetime
from typing import Optional


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


# defining a class using pydantic each attribute represent a data field and has the type.
class DataItems(BaseModel):
    id: Optional[int]
    timestamp: datetime.time
    age: Optional[str]
    industry: Optional[str]
    job_title: Optional[str]
    job_context: Optional[str]
    annual_salary: Optional[float]
    additional_compensation: Optional[str]
    currency: Optional[str]
    currency_other: Optional[str]
    income_context: Optional[str]
    country: Optional[str]
    us_state: Optional[str]
    city: Optional[str]
    years_experience_overall: Optional[str]
    years_experience_field: Optional[str]
    education_level: Optional[str]
    gender: Optional[str]
    race: Optional[str]
