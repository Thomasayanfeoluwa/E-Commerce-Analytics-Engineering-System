import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def run_sql(query:str) -> pd.DataFrame:
    return pd.read_sql(text(query), engine)
