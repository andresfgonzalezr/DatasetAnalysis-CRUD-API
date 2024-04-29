import pandas as pd
from sqlalchemy import create_engine


db_url = "postgresql://default:VbwkxX41WTuY@ep-polished-frost-a41zn8lf-pooler.us-east-1.aws.neon.tech:5432/verceldb"
engine = create_engine(db_url)
sql_query = "SELECT * FROM survey"
df = pd.read_sql(sql_query, engine)


db_url = "postgresql://default:VbwkxX41WTuY@ep-polished-frost-a41zn8lf-pooler.us-east-1.aws.neon.tech:5432/verceldb"
engine_1 = create_engine(db_url)
sql_query = "SELECT * FROM final_data_andres"
df_final1 = pd.read_sql(sql_query, engine)