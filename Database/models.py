from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from pydantic import BaseModel  # type: ignore
from typing import Optional

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    dni = Column(Integer, unique=True, index=True)
    email = Column(String, unique=True, index=True)

# Define el esquema de datos de entrada para el usuario
class UserIn(BaseModel):
    username: str
    email: str
    password: str
    dni: int

class LoginRequest(BaseModel):
    email: str
    password: str

class getCurrentRequest(BaseModel):
    id: int

class deleteRequest(BaseModel):
    token: str

class TokenData(BaseModel):
    email: Optional[str] = None