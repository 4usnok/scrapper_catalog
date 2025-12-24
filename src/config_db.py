import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

NAME_DB = os.getenv("dbname")
HOST_DB = os.getenv("host")
USER_DB = os.getenv("user")
PASSWORD_DB = os.getenv("password")
PORT_DB = os.getenv("port")

db_save = f"postgresql+psycopg2://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"
engine = create_engine(db_save)
table_name = "web_scrapper"
