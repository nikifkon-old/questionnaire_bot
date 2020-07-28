from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config


def get_db_url(db, username, password, host, port, db_name):
    return f"{db}://{username}:{password}@{host}:{port}/{db_name}"


postgres_url = get_db_url(
    db="postgres",
    username=Config.DATABASE_USERNAME,
    password=Config.DATABASE_PASSWORD,
    host=Config.DATABASE_HOST,
    port=Config.DATABASE_PORT,
    db_name=Config.DATABASE_NAME
)

engine = create_engine(postgres_url, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
