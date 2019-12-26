# CodersLab-Workshop_2
This repository contains a simple command line messenger application utilizing the Python argparse module. The aim of writing the app was to get familiar with Python handling of the following:
- databases
- object oriented programming
- basic password hashing
- argparse module

The app is designed to be run from the command line interface, e.g. the Ubuntu terminal.

The repository contains the following files:
- models.py - contains the User and Message class with their attributes and methods as well as the connect_to_db function which returns the database connection. There are two TODO's in the function - the user needs to input their database username and password in the code;
- users.py - basic user login interface with functionality to add, delete, edit and list users
- messages.py - messenger interface allowing to send and list messages which are being stored in the database
- requirements.txt - list of packages installed in the virtual environment for running the app. Not all are required - psycopg2 is the key one for handling the database queries
- db_backup.sql - the backup drop of my database used for running the app
