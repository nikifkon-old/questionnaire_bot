from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import config


def get_db_url(db, username, password, host, port, db_name):
    return f"{db}://{username}:{password}@{host}:{port}/{db_name}"


postgres_url = get_db_url(
    db="postgres",
    username=config.get("database", "username"),
    password=config.get("database", "password"),
    host=config.get("database", "host"),
    port=config.get("database", "port"),
    db_name=config.get("database", "name"),
)

engine = create_engine(postgres_url, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
