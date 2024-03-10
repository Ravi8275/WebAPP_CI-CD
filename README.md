# WebAPP With FastAPI

# Introduction
The project demonstrates the integration of FastAPI webframework for building API with python and Postgresql for Database management.The Application allows users to Register,perform login operations and update their information seamlessly using corresponding API endpoints.

## Feature Description
- **Health Check Endpoint**('/healthz')-Provides a health check endpoint to ensure the application and database are connected and running properly.
- **Registration Endpoint**('/Registration' endpoint)-Allows users to register by providing their First name,Last name,Email ID, and password.
- **Client Login Endpoint**('/Client Login' endpoint)-Allows registered users to login by providing their email id and password.
- **Update Client Details Endpoint**('/Client/Update endpoint)-Allows users to update their details such as password, First name, and Last name.

## Technologies Used
- **FastAPI**- A Webframework for building API's with python 3.7+ and allows for easy creation of asynchronous APIs with automatic interactive API documentation via Swagger UI.
- **Postgresql**- Open Source object-relational database known for it's reliability and robustness.