from fastapi import status
from fastapi.testclient import TestClient
from main import application
import requests

client = TestClient(application)


def test_client():
    response = client.get('/v1/healthz')
    assert response.status_code == status.HTTP_200_OK


def test_create_account():
    response=requests.post('v1/user',json={'First_Name':'john','Second_Name':'Wick','Email_id':'Johnwick@gmail.com','password':'secret'})
    assert response.status_code== status.HTTP_201_CREATED

def test_update_account():
    response=requests.put('/v1/user/{Email_id}',json={'First_Name':'john','Second_Name':'Wick','Email_id':'Johnwick@gmail.com','password':'secret','New_password':'no secret'})
    assert response.status_code== status.HTTP_200_OK
