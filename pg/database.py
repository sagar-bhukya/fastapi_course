#ORM(Object-relational-mapping)
#FastAPI works with any database and any style of library to talk to the database.
#A common pattern is to use an "ORM": an "object-relational mapping" library.
#An ORM has tools to convert ("map") between objects in code and database tables ("relations").
#With an ORM, you normally create a class that represents a table in a SQL database, each attribute of the class represents a column, with a name and a type
#For example a class Pet could represent a SQL table pets.
#Common ORMs are for example: Django-ORM (part of the Django framework), SQLAlchemy ORM (part of SQLAlchemy, independent of framework) and Peewee (independent of framework), among others.

#SQLAlchemy is an open-source SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of high-level API (Application Programming Interface) to interact with relational databases, making it easier to manage database operations and interact with databases using Python code.
#1:pip install sqlalchemy
from fastapi import create_engine
#--------
#create_engine:create_engine is a function provided by SQLAlchemy that is used to create a database engine. The engine serves as the interface between your Python application and the relational database. It provides a way to communicate with the database, execute SQL statements, and manage connections.
#--------
from sqlalchemy.ext.declarative import declarative_base
#declarative_base:declarative_base is a class provided by SQLAlchemy that serves as a base class for declarative class definitions. In SQLAlchemy, the declarative base is used to define ORM (Object-Relational Mapping) models in a more concise and high-level manner.
from sqlalchemy.orm import sessionmaker
#sessionmaker:sessionmaker is a class provided by SQLAlchemy that is used to create session factories. A session, in the context of SQLAlchemy, is a workspace for interacting with the database. Sessions are used to manage database transactions and provide a high-level interface for querying and manipulating the database.
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
SQL_DATABASE_URL="postgresql://postgres:Sagar@123localhost/dvdrental"
engine=create_engine(SQL_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
