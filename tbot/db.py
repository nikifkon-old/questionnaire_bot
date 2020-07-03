from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import config

sqlite_file_path = config["database"]["sqlite_file_path"]
engine = create_engine("sqlite:///%s" % sqlite_file_path,
                       echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
