import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


db_url_1 = "postgresql://default:VbwkxX41WTuY@ep-polished-frost-a41zn8lf-pooler.us-east-1.aws.neon.tech:5432/verceldb"
engine_1 = create_engine(db_url_1)
sql_query = "SELECT * FROM survey"
df_for_clean = pd.read_sql(sql_query, engine_1)
sql_query_1 = "SELECT * FROM final_data_andres"
df_final1 = pd.read_sql(sql_query_1, engine_1)


Base = declarative_base()

Base.metadata.create_all(bind=engine_1)
SessionLocal = sessionmaker(bind=engine_1)
session = SessionLocal()