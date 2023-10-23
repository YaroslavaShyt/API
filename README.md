# Instalations
- pip install grpcio grpcio-tools
- pip install python-dotenv
- pip install sqlalchemy[asyncio]

# Database
- Database settings:
- MySQL(тимчасово)

- CREATE DATABASE GEORESEARCH;

- CREATE TABLE PROJECTS(
- 	ID INT auto_increment PRIMARY KEY,
-     NAME VARCHAR(255),
-    DESCRIPTION VARCHAR(255),
-    TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-    STATUS VARCHAR(255)
-);

# Run
- Terminal 1: python server.py
- Terminal 2: python client.py
