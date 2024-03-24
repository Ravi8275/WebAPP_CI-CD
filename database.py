from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean,Sequence
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
import os
import subprocess
from datetime import datetime
from fastapi import FastAPI, HTTPException,status, Request,Depends

load_dotenv()

LocalDatabase_URL=os.getenv("DATABASE_URL")

Engine = create_engine(LocalDatabase_URL)

Base_model = declarative_base()

Localsession = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

def start_db():
    DB = Localsession()
    try:
        yield DB
    finally:
        DB.close()

def Database_Connection_check():
    try:
        Connection_creation = create_engine(LocalDatabase_URL)
        with Connection_creation.connect():
            return status.HTTP_200_OK
    except OperationalError:
        return status.HTTP_503_SERVICE_UNAVAILABLE

class Clients(Base_model):
    __tablename__ = "clients" 

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    account_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)