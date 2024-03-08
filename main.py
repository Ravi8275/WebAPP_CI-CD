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

#Base_model.metadata.create_all(bind=create_engine(LocalDatabase_URL))

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

@application.get("/healthz", status_code=status.HTTP_200_OK)
async def Health_check(request: Request):
    if request.query_params or await request.body():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no payload allowed")
    if Database_Connection_check() == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    headers = {
        "Cache-Control": "no-cache"
    }
    return {}, headers


@application.post("/Register", status_code=status.HTTP_201_CREATED)
async def Client_Registration(First_Name: str, Second_Name: str, Email_id: str, password: str):
    DB = Localsession()
    Existing_client = DB.query(Clients).filter(Clients.email == Email_id).first()
    if Existing_client:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client already exists")
    New_client = Clients(email=Email_id, password=password, first_name=First_Name, second_name=Second_Name)
    DB.add(New_client)
    DB.commit()
    Client_Details={
        'Email':Email_id,
        'Name':First_Name+' '+Second_Name
    }
    return {"Info" : "User registered Successfully","Client_Details": Client_Details}

@application.get("/Client login")
async def Client_login(Email_id: str, password: str, db: Session = Depends(start_db)):
    Check_details = db.query(Clients).filter(Clients.email == Email_id, Clients.password == password).first()    
    if Check_details:
        Current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Client_Loggedin_details={
        'Email':Email_id,
        'Name':Check_details.first_name+' '+Check_details.second_name,
        'Unique ID':Check_details.id,
        'Logged in time':Current_time
        }
        return {"Message": "Logged in Successfully",'Client_details':Client_Loggedin_details}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email id or password")

@application.put("/Client/update",status_code=status.HTTP_200_OK)
async def Update_Client_Details(
    Email_id:str, 
    Old_password:str, 
    New_password:str, 
    New_first_name:str, 
    New_second_name:str,
    db: Session=Depends(start_db)
):
    client=db.query(Clients).filter(Clients.email==Email_id,Clients.password==Old_password).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Client not found or invalid credentials")
    client.password=New_password
    client.first_name=New_first_name
    client.second_name=New_second_name
    db.commit()
    return {"message": "Client details updated successfully"}

