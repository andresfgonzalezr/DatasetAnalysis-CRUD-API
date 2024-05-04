import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker, declarative_base


db_url = "postgresql://default:VbwkxX41WTuY@ep-polished-frost-a41zn8lf-pooler.us-east-1.aws.neon.tech:5432/verceldb"
engine = create_engine(db_url)
sql_query = "SELECT * FROM survey"
df_for_clean = pd.read_sql(sql_query, engine)


#db_url = "postgresql://default:VbwkxX41WTuY@ep-polished-frost-a41zn8lf-pooler.us-east-1.aws.neon.tech:5432/verceldb"
#engine_1 = create_engine(db_url)
#sql_query = "SELECT * FROM final_data_andres"
#df_final1 = pd.read_sql(sql_query, engine)


load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


Base = declarative_base()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()