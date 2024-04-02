# WebAPP With FastAPI

# Introduction
The project demonstrates the integration of FastAPI webframework for building API with python and Postgresql for Database management.The Application allows users to Register and update their information seamlessly using corresponding API endpoints.

## Feature Description
- **Health Check Endpoint**('/healthz')-Provides a health check endpoint to ensure the application and database are connected and running properly.
- **Registration Endpoint**('/Registration' endpoint)-Allows users to register by providing their First name,Second name,Email ID, and password.
- **Update Client Details Endpoint**('/Client/Update endpoint)-Allows users to update their details such as password, First name, and Second name.

## Technologies Used
- **FastAPI**- A Webframework for building API's with python 3.7+ and allows for easy creation of asynchronous APIs with automatic interactive API documentation via Swagger UI.
- **Postgresql**- Open Source object-relational database known for it's reliability and robustness.

## Requirements 
- **Python 3.x**
- **FastAPI**
- **Uvicorn**


## Installations

### To get start with the project,start with cloning the repository

```
git clone https://github.com/your_username/your_repository.git
```

### Navigate to Project Directory

cd your_repository

### Install Dependencies
```
pip install -r requirements.txt
```
Setup PostgreSQL
Create User with password using
```
CREATE USER webappcicd WITH PASSWORD 'webappcicd';

```

Create the database

```
CREATE DATABASE mydatabase;
```
Create Appropriate schema using
```
CREATE TABLE clients (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    second_name VARCHAR,
    account_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    account_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

 Create Virtual Environment using
```
touch .env
```

Store the Configuration variables like database url in the environment file
```
DATABASE_URL=postgresql://username:password@localhost:5432/databasename
```
Make sure to replace the username,password and databasename with the appropriate values.

### Run the Application 
```
uvicorn main:application --reload
```
## Accessing the API
Once the application is running, one can access the API endpoints using a web browser or tools like Postman. 

The base URL for the API will typically be http://localhost:8000.

# API Endpoints:
Refer to the API documentation or explore all the available endpoints using tools like Swagger UI or ReDoc, 
which are usually accessible at http://localhost:8000/docs or http://localhost:8000/redoc.












