from fastapi import FastAPI, HTTPException,status, Request,Depends
from fastapi.responses import JSONResponse
import subprocess
import logging
from pydantic import BaseModel
import bcrypt
import uuid
from database import start_db,Database_Connection_check,Base_model,Clients
from sqlalchemy.orm import  Session

application=FastAPI()

@application.get("/v1/healthz", status_code=status.HTTP_200_OK)
async def Health_check(request: Request):
    if request.query_params or await request.body():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no payload allowed")
    if Database_Connection_check() == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    headers = {
        "Cache-Control": "no-cache"
    }
    return None

@application.put("/v1/healthz", status_code=status.HTTP_200_OK)
async def Health_check(request: Request):
    if request.query_params or await request.body():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no payload allowed")
    if Database_Connection_check() == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    headers = {
        "Cache-Control": "no-cache"
    }
    return None

@application.post("/v1/healthz", status_code=status.HTTP_200_OK)
async def Health_check(request: Request):
    if request.query_params or await request.body():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no payload allowed")
    if Database_Connection_check() == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    headers = {
        "Cache-Control": "no-cache"
    }
    return None

@application.delete("/v1/healthz", status_code=status.HTTP_200_OK)
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
 
@application.post("/v1/user", status_code=status.HTTP_201_CREATED)
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

@application.put("/v1/user/{Email_id}",status_code=status.HTTP_200_OK)
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

