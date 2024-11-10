from sqlalchemy import create_engine, MetaData  # type: ignore
from databases import Database  # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from config import DATABASE_URL

# Configuración de la base de datos
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
