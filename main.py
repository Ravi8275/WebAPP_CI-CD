from fastapi import FastAPI,HTTPException,status,Request
#Importing HTTPException inorder to handle errors i.e Exceptions and to inform user about the error
from sqlalchemy import create_engine
#Importing create_engine to create SQLalchemy engine inorder to establish database connections
from sqlalchemy.exc import OperationalError
#Importing OperationalError to handle the exceptions in the case of operational failure with the database
from sqlalchemy.orm import sessionmaker
#Importing sessionmaker to create session factories which are used to manage database session in SQLalchemy
from dotenv import load_dotenv
#To load other environment variables into the file
import os


application=FastAPI() 
#instance creation for FastAPI for further use throughout route definitions and to run the Fastapi application

load_dotenv()
#Loading environment variables

postgres_password=os.getenv("POSTGRES_PASSWORD")
#Variable initialisation for the desired input.

LocalDatabase_URL="postgresql://webappcicd:webappcicd@localhost:5432/postgres"
#Providing the Postgresql Database url for the connection

#Connectivity Check Function
#Function definition
def Database_Connection_check():
    try:
        Connection_creation=create_engine(LocalDatabase_URL)
        #Creating the SQLalchemy engine to further create the connection by passing Mentioned url as a parameter to create_engine function

        with Connection_creation.connect():
            return status.HTTP_200_OK
        #Establishing the Connection with connect method using the Sqlalchemy engine which was created earlier.
    except OperationalError:
        return status.HTTP_503_SERVICE_UNAVAILABLE

#if the connection with the desired database is made successully then True would be returned and False incase of failure.

#Enpoint For Health check

@application.get("/healthz",status_code=status.HTTP_200_OK)
#Defining the route for get function to 'healthz'endpoint
#Status code HTTP 200 ok indicates the successful connection with the endpoint.
async def Health_check(request : Request):
    if request.query_params or await request.body(): #To check for inappropriate requests 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="no payload allowed")
    # Handler function whenever the 'healthz' endpoint is called
    if Database_Connection_check()==status.HTTP_503_SERVICE_UNAVAILABLE:  #Connection establishment check with the help of response from previous code block
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        # HTTP 503 status unavailable will be returned in case of failed connection if not status code mentioned within the health endpoint will be returned
    headers = {
        "Cache-Control": "no-cache"
    }
    # To ensure API return will provide the up-to-date information and not the cache information
    return {}, headers

#Defining the root endpoint for landing page
@application.get('/')
def read_root():
    return{"message":"welcome to the fast api application"}

#Defining methods which are not allowed to operate by the user
@application.post('/')
@application.put('/')
@application.patch('/')
async def Dummy_Methods():#Handling function for defined methods
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        #Defining status code for Dummy Methods.
    )