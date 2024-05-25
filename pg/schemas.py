#Create initial Pydantic models / schemas
'''Create an ItemBase and UserBase Pydantic models (or let's say "schemas") to have common attributes while creating or reading data.
And create an ItemCreate and UserCreate that inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.
So, the user will also have a password when creating it.
But for security, the password won't be in other Pydantic models, for example, it won't be sent from the API when reading a user.'''
from typing import List, Union
from pydantic import BaseModel# Import the BaseModel class from the Pydantic library
## Define the base class for items using Pydantic
class ItemBase(BaseModel):
    # Define the properties for an item
    title:str
    description:Union[str,None]=None# Union allows for a string or None for the description
# Define a class for creating items, inheriting from ItemBase
class ItemCreate(ItemBase):
    pass
# Define a class representing an item, including its ID and owner ID
class Item(ItemBase):
    id:int
    owner_id:int
    # Configure Pydantic to work in ORM mode
    class Config:
        orm_mode:True
# Define the base class for users using Pydantic
class UserBase(BaseModel):
    # Define the property for a user's email
    email:str
# Define a class for creating users, inheriting from UserBase
class UserCreate(UserBase):
     # Include a property for the user's password when creating a user
    password:str
# Define a class representing a user, including ID, whether they are active, and a list of items
class User(UserBase):
    id:int
    is_active:bool
    items:List[Item]# A list of items associated with the user
     # Configure Pydantic to work in ORM mode
    class Config:
        orm_mode=True

