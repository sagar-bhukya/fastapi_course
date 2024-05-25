#Create the database models
from .database import Base
from sqlalchemy import Boolean,Column,ForeignKey,Integer,String,primary_key
from sqlalchemy.orm import relationship

# Define the User class that inherits from the Base class
class User(Base):
    # Specify the name of the corresponding database table
    __tablename__="users"
    # Define Columns for the 'users' table
    id=Column(Integer,primary_key=True)# Primary key for the user
    email=Column(String,unique=True,index=True)# Unique email for each user, indexed for faster queries
    hashed_password=Column(String)# Hashed password for user security
    is_active=Column(Boolean,default=True)## Boolean flag to indicate if the user is active
    
    # Define a relationship with the 'Item' class, establishing a one-to-many relationship
    items=relationship("Item",back_populates="owner")

# Define the Item class that also inherits from the Base class
class Item(Base):
    # Specify the name of the corresponding database table
    __tablename__="items"
    # Define Columns for the 'items' table
    id=Column(Integer,primary_key=True) # Primary key for the item
    title=Column(String,index=True)# Title of the item, indexed for faster queries
    description = Column(String, index=True)# Description of the item, indexed for faster queries
    owner_id=Column(Integer,ForeignKey("users.id")) # Foreign key referencing the 'id' column in the 'users' table
    owner=relationship("User",back_populates="users")


