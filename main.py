from fastapi import FastAPI, HTTPException, status, Request,Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean,Sequence
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from fastapi.responses import JSONResponse
import subprocess
import uuid
import logging
from pydantic import BaseModel
import bcrypt

application=FastAPI()
 
load_dotenv()

postgres_password=os.getenv("POSTGRES_PASSWORD")

LocalDatabase_URL="postgresql://webappcicd:webappcicd@localhost:5432/clientdatabase"

homebrew_executable="/opt/homebrew/bin/brew"

def start_postgresql():
    try:
        subprocess.run([homebrew_executable,"services","start","postgresql"],check=True)
        print("PostgreSQL service started successfully.")
    except subprocess.CalledProcessError as e: 
        print(f"Error starting PostgreSQL service:{e}")   
start_postgresql()
Base_model=declarative_base()

class Clients(Base_model):
    __tablename__ = "clients" 

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    account_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

Base_model.metadata.create_all(bind=create_engine(LocalDatabase_URL))

Localsession = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(LocalDatabase_URL))

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s- %(message)s",
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

@application.get("/healthz", status_code=status.HTTP_200_OK)
async def Health_check(request: Request):
    if request.query_params or await request.body():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no payload allowed")
    if Database_Connection_check() == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    headers = {
        "Cache-Control": "no-cache"
    }
    return None

@application.put("/healthz", status_code=status.HTTP_200_OK)
async def Health_check(request: Request):
    if request.query_params or await request.body():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no payload allowed")
    if Database_Connection_check() == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    headers = {
        "Cache-Control": "no-cache"
    }
    return None

@application.post("/healthz", status_code=status.HTTP_200_OK)
async def Health_check(request: Request):
    if request.query_params or await request.body():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no payload allowed")
    if Database_Connection_check() == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    headers = {
        "Cache-Control": "no-cache"
    }
    return None

@application.delete("/healthz", status_code=status.HTTP_200_OK)
async def Health_check(request: Request):
    if request.query_params or await request.body():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no payload allowed")
    if Database_Connection_check() == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    headers = {
        "Cache-Control": "no-cache"
    }
    return None

  # password hashing functions
def get_password_hash(password):
    pwd_bytes = password.encode('utf-8') #utf-8 is similat to byte repsentation of text i.e b"password"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    string_password = hashed_password.decode('utf8')
    return string_password  

def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8') #Similarly mentining the byte representation using utf-8 encoding
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password)


class ClientRegistrationRequest(BaseModel):
    First_Name: str
    Second_Name: str
    Email_id: str
    password: str
 
@application.post("/Register", status_code=status.HTTP_201_CREATED)
async def Client_Registration(Client_data:ClientRegistrationRequest,db:Session=Depends(start_db)):
    First_Name=Client_data.First_Name
    Second_Name=Client_data.Second_Name
    Email_id=Client_data.Email_id
    password=Client_data.password
    if not all([First_Name,Second_Name,Email_id,password]):
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incomplete user registration data")
    Existing_client=db.query(Clients).filter(Clients.email == Email_id).first()
    if Existing_client:
        logging.error("Client already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client already exists")
    hashed_password=get_password_hash(password)
    client_id=str(uuid.uuid4())
    New_client=Clients(id=client_id,email=Email_id, password=hashed_password, first_name=First_Name, second_name=Second_Name)
    db.add(New_client)
    db.commit()
    Client_Details={
        'Email':Email_id,
        'Name':First_Name+' '+Second_Name
    }
    return {"Info" : "User registered Successfully","Client_Details": Client_Details}


class ClientUpdateRequest(BaseModel):
    Email_id:str
    password:str
    New_password:str
    First_Name: str
    Second_Name: str

@application.put("/Client/update",status_code=status.HTTP_200_OK)
async def Update_Client_Details(Client_data:ClientUpdateRequest,db:Session=Depends(start_db)):
    Email_id=Client_data.Email_id
    Old_password=Client_data.password
    New_password=Client_data.New_password
    New_first_name=Client_data.First_Name 
    New_second_name=Client_data.Second_Name
    if not all([Email_id,Old_password,New_password,New_first_name,New_second_name]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incomplete client update data")
    client=db.query(Clients).filter(Clients.email==Email_id).first()
    if not client or not verify_password(Old_password, client.password):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Client not found or invalid credentials")
    hashed_new_password=get_password_hash(New_password)
    client.password=hashed_new_password
    client.first_name=New_first_name
    client.second_name=New_second_name
    db.commit()
    return {"message": "Client details updated successfully"}

