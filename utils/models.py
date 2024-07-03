from pydantic import BaseModel
from typing import Optional


# defining a class using pydantic each attribute represent a data field and has the type.
class DataItems(BaseModel):
    id: Optional[int]
    timestamp: Optional[str]
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


class InputData(BaseModel):
    age = str
    industry = str
    currency = str
    country = str
    us_state = str
    city = str
    years_experience_overall = str
    years_experience_field = str
    education_level = str
    gender = str
    race = str
