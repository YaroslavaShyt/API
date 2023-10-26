# Instalations
- pip install grpcio grpcio-tools
- pip install python-dotenv
- pip install sqlalchemy[asyncio]
- pip install pymssql


# Database
- Database settings:
- Download Ms SQL Server 2022, Ms SQL Server Management Studio
- Create database georesearch, table projects:
- CREATE DATABASE GEORESEARCH;
- CREATE TABLE PROJECTS(
	ID INT PRIMARY KEY IDENTITY(1, 2),
	NAME VARCHAR(70),
	DESCRIPTION VARCHAR(70),
	CREATED DATETIME DEFAULT GETDATE(),
	STATUS VARCHAR(10)
);

# Python connection settings
- in file .env change parametr SERVER to yours (shown in ms sql server management studio, in dialog box)
- 
# Run
- Terminal 1: python server.py
- Terminal 2: python client.py
