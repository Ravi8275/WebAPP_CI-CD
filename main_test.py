from fastapi import status
from fastapi.testclient import TestClient
from main import application
import requests

client = TestClient(application)


def test_client():
    response = client.get('/healthz')
    assert response.status_code == status.HTTP_200_OK


def test_create_account():
    response=requests.post('http://localhost:8000/v1/user',json={'First_Name':'John','Second_Name':'Wick','Email_id':'Johnwick@gmail.com','password':'secret'})
    assert response.status_code== 201

def test_update_account():
    response=requests.put('http://localhost:8000/v1/user/1',json={'First_Name':'John','Second_Name':'Wick','Email_id':'Johnwick@gmail.com','password':'secret','New_password':'no secret'})
    assert response.status_code== 200

def test_get_account():
    response.get('http://localhost:8000/v1/user/1')
    assert response.status_code==200
    assert response.json()['Email_id']=='Johnwick@gmail.com'