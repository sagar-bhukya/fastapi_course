from fastapi import FastAPI

app =FastAPI()

@app.get('/')
def home():
    return {'name':'sagar',"age":22}

@app.get('/items/')
def list_items():
    return {"car":"bMw","engine":"Petrol"}
#path parameters
@app.get('/item/{item_id}')
async def readitems(item_id):
    return {"item_id":item_id}
#path parameters with type
@app.get('/item_type/{item_id}')
async def read_item_type(item_id:int):
    return {"item_id":item_id}
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

#Query Parameters
#Query parameters in FastAPI allow you to pass additional data to your API endpoints through the URL. They are commonly used for filtering, sorting, or providing additional options to your API.

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/item1")
async def query_parameter(skip:int=0,limit:int=2):
    return fake_items_db[skip : skip+limit]
#Optional Query Parameter:
@app.get('/item1/{item_id}')
async def opt_query(item_id:str,q:str|None=None):
    if q:
        return {"item_id":item_id,"Optional_q":q}
    return {"item_id",item_id}

#Query parameter type conversion
@app.get('/item2/{item_id}')
async def type_conversinfg(item_id:str, q:str|None=None,short:bool=False):
    item={"item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description":"my name is sagar bhukya"}
        )
    return item

#Multiple path and query parameters
@app.get('/item3/{item_id}/user1/{user_id}')
async def multi_query(item_id:int,user_id:int,q:str|None=None,short:bool=False):
    item={"item_id":item_id,"owner_id":user_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update({"description":"i am sagar bhukya working as a software developer"})
    return item

#Required query parameters
@app.get('/item4/{item_id}')
async def re_par(item_id:str,needy:str):
    item={"item_id":item_id,"needy":needy}
    return item

#Pydantic makes sure the data your application deals with is structured the way you expect, helping you avoid unexpected surprises and ensuring the smooth operation of your code.
#Request Body¶
'''When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

A request body is data sent by the client to your API. A response body is the data your API sends to the client.

Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time.'''
from pydantic import BaseModel
from typing import Optional
class Item(BaseModel):
    name:str
    # descr:str|None=None
    descr:Optional[str]=None
    price:float
    tx:float| None=None
@app.post('/itrem5/')
async def req_par(item:Item):
    return item

#Use the model¶
#Inside of the function, you can access all the attributes of the model object directly:
@app.post('/item6/')
async def inside_function(item:Item):
    item_dict=item.dict()
    if item.tx:
        price_with_tax=item.tx+item.price
        item_dict.update({"updated with price_with_trax":price_with_tax})
    return item_dict

#Request body + path parameters
@app.put('/item8/{item_id}')
async def req_path(item_id:int,item:Item):
    return {"item_id":item_id,**item.dict()}

#Request body + path + query parameters
@app.put('/item9/{item_id}')
async def req_path_quer(item_id:int,item:Item,q:str|None=None):
    item_new={"item_id":item_id,**item.dict()}
    if q:
        item_new.update({"q":q})
    return item_new

#Query Parameters and String Validations
@app.get("/item10/")
async def query_p_str_valid(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
# #Additional validation
from typing import Annotated
from fastapi import Query
# @app.get("/items11/")
# async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

#Path Parameters and Numeric Validations
from fastapi import Path
@app.get("/items13/{item_id}")
async def path_par_Nume_par(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

#Body - Multiple Parameters
#Mix Path, Query and body parameters

class Sagar(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def mix_path_quer_body(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Sagar | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results 

#Multiple body parameters
class a(BaseModel):
    name:str
    age:int
class b(BaseModel):
    surname:str
    rollna:str
@app.put('/items14/{item_id}')
async def mult_body_pars(item_id:int,A:a,B:b):
    result={"item_id":item_id,"a":A,"b":B}
    return result
#Body - Nested Models-------------
class address(BaseModel):
    vil:str
    street:str
    state:str
    pin:int
class User(BaseModel):
    name:str
    age:int
    address:address
@app.post('/create_user/')
async def body_nested_models(user:User):
    user_data=user.dict()
    return {"user_details":user_data}

#type parameter basemodel
class data(BaseModel):
    name:str
    desc:str
    price:str
    tax:float|None=None
    tags:list[str]=[]
@app.put('/data/{item_id}')
async def data_list(item_id:int,Data:data):
    result={"item_id":item_id,"Data":Data}
    return result

#nested_models with type
from typing import Union
from pydantic import HttpUrl
class Image(BaseModel):
    # url:str
    url:HttpUrl
    name:str
class Image_main(BaseModel):
    name:str
    desc:Union[str,None]=None
    price:float
    tax:Union[str,None]=None
    image:Union[Image,None]=None
@app.put('/image/{item_id}')
async def image(item_id:int,image_cl:Image_main):
    res={"item_id":item_id,"image":image_cl}
    return res

#specialtype HttpUrl and list of Image
@app.put('/specialtype/{item_id}')
async def specialtype(item_id:int,image:Image_main):
    return {"item_id":item_id,"Image":image}


#Deeply nested models
class a(BaseModel):
    a:str
    b:str|None=None
class b(BaseModel):
    c:str
    d:list[a]
class c(BaseModel):
    e:str
    f:list[b]
@app.post('/Deeply_nested_models/{item_id}')
async def deeply_nest_models(item_id:int,C:c):
    return {"item":item_id,"C":C}

#Bodies of pure lists
class mul(BaseModel):
    i:HttpUrl
    name:str
@app.post('/img/multiple/')
async def multiple_img(img:list[mul]):
    return img

#Declare Request Example Data
# class re(BaseModel):
#     name:str
#     age:int
# data={
#     "name":"Sagar",
#     "designation":"Python Developer",
#     "Roll_id":"20079"
# }
# @app.post('/res_declaration/{item_id}')
# async def dec_req(item_id:int,Data:re=data):
#     return {"item":item_id,"Data":Data}
class I(BaseModel):
    name: str
    description: str = None
    price: float
    tags: list[str] = []

# Example request data
example_request_data = {
    "name": "Example Item",
    "description": "This is an example item.",
    "price": 19.99,
    "tags": ["example", "test"]
}
@app.post("/create_item")
async def create_item(item: Item = example_request_data):
    return {"item": item}

#Extra Data Types
#Optional:
@app.post('/optional/')
async def optinal(name: Optional[str]=None)->str:
    if name:
        return f"Hello,{name}"
    else:
        return "good bye"
#List
@app.post('/list_sum/')
async def lsit_sum(numbers:list[int])->int:
    return sum(numbers)
    
from datetime import datetime,time,timedelta
from uuid import UUID
from fastapi import Body
@app.put("/mult_data/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[Union[datetime, None], Body()] = None,
    end_datetime: Annotated[Union[datetime, None], Body()] = None,
    repeat_at: Annotated[Union[time, None], Body()] = None,
    process_after: Annotated[Union[timedelta, None], Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

#Cookie Parameters----
#you can use cookie parameters to handle cookies sent in the HTTP request. Cookies are small pieces of data sent from a server and stored in the user's browser. They can be included in subsequent requests to provide additional information or maintain state.
# FastAPI route with a cookie parameter
from fastapi import FastAPI, Cookie

@app.get("/read_cookie")
async def read_cookie(cookie_value: str = Cookie(default=None)):
    return {"cookie_value": cookie_value}
@app.get("/read_cock/")
async def read_items(ads_id: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_id}

#Header Parameters
# you can use header parameters to handle information sent in the headers of an HTTP request. Headers are typically used for information like authentication tokens, content type negotiation, and other metadata. 
from fastapi import Header
@app.get('/read_hearder/')
async def read_header(api_key:str=Header(default=None,description="API key")):
    return {"api_key":api_key}

#Response Model - Return Type------
class It(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# FastAPI route with a response model
@app.get("/response", response_model=It)
async def read_item():
    item_data = {
        "name": "Example Item",
        "description": "This is an example item.",
        "price": 19.99,
        "tax": 2.00
    }
    return item_data
#1
class resp(BaseModel):
    name:str
    price:float
    tags:list[str]=[]
@app.post("/response_items/")
async def response_return(item:resp)->resp:
    return item
@app.get("/response_read/")
async def response_read_return()->list[resp]:
    return [
        resp(name="biscuit", price=42.0),
        resp(name="fizz", price=20.8),
    ]

#Add an output model
from pydantic import EmailStr
from typing import Any
class userin(BaseModel):
    username:str
    password:str
    email:EmailStr
    fullName:str|None=None
class userout(BaseModel):
    username:str
    email:EmailStr
    fullName:str|None=None
@app.post("/user_data/",response_model=userout)
async def add_output(item:userin):
    return item

#Return Type and Data Filtering
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
class Use(BaseUser):
    password: str
    username:str
@app.post('/user_data1/')
async def data_filter(item:Use)->BaseUser:
    return item

#Extra Models---------------
#Multiple models
#Here's a general idea of how the models could look like with their password fields and the places where they are used:
class User_In(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class User_Out(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

def fake_password_hasher(raw_password:str):
    return "super_secret"+raw_password
def fake_save_user(user_in:User_In):
    hashed_password=fake_password_hasher(user_in.password)
    user_in_db=UserInDB(**user_in.dict(),hashed_password=hashed_password)
    print("user saved!.....not really")
    print("user_in",user_in.dict())
    return user_in_db
@app.post('/user_log_in/',response_model=User_Out)
async def create_user(user_in:User_In):
    user_saved=fake_save_user(user_in)
    return user_saved

class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

#Union or anyOf
from typing import Union
class Aa(BaseModel):
    desc:str
    type:str
class Bb(Aa):
    type:str="car"
class Cc(Aa):
    type:str="Bike"
    size:int

items={
    "item1":{"desc":"here am doing the connection","type":"car"},
    "item2":{"desc":"this one is addition of that","type":"Bike","size":37}
}
@app.get('/connection/{item_id}',response_model=Union[Bb,Cc])
async def connection_union(item_id:int):
    return items[item_id]


#List of models==
from typing import List
class lis(BaseModel):
    name:str
    desc:str
item_data=[
    {"name":"sagar","desc":"sagarbhukya software developer"},
    {"name":"vennela","desc":"she is my sister"}
]
@app.get('/list_data/',response_model=List[lis])
async def list_itemdata():
    return item_data

#Response Status Code-----
@app.post('/http_200/',status_code=200)
async def OK(name:str):
    return {"name":name}

@app.post('/http_201/',status_code=201)
async def Created(name:str):
    return {"name":name}

#statu importt
from fastapi import status
@app.post("/short_cut_status_code/",status_code=status.HTTP_404_NOT_FOUND)
async def shortcut(name:str):
    return {"name":name}

#Form Data
# form data refers to data that is submitted through HTML forms. When a user submits a form on a website, the form data is sent in the body of the HTTP request. FastAPI provides a way to handle and parse form data in your route functions.
from fastapi import Form
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
@app.post("/create_user")
async def create_user(username: str = Form(...), email: str = Form(...)):
    return {"username": username, "email": email}   
@app.post("/submit_form/")
async def submit(username:str=Form(...),password:str=Form(...)):
    return {"username": username, "password": password}

#Request Files------------
#In FastAPI, you can handle file uploads using the File class. The File class allows you to receive files as part of an HTTP request. Here's a brief overview of handling request files in FastAPI:
from fastapi import File,UploadFile
@app.post("/file/")
async def file(file:Annotated[bytes,File()]):#Define File Parameters
    return {"file_size":file}
@app.post("/file1/")
async def file1(file:UploadFile):#File Parameters with UploadFile
    return {"filename":file.filename}
#Optional File Upload
@app.post("/file_upload/")
async def file_upload(file:Annotated[bytes,File()]=None):
    if not file:
        return {"message":"no file"}
    else:
        return {"size_file":len(file)}
@app.post("/file_upload1/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
    
@app.post("/additional_data/")
async def additional_data(file:Annotated[bytes,File(description="this file about json")]):#additional data
    return {"file_len":len(file)}
@app.post("/additional1/")
async def additiona2(file:Annotated[UploadFile,File(description="this is about html")]):#additional data
    return {"filename":file.filename}

#Multiple File Uploads-------------
@app.post("/mul_files/")
async def mul_files(file:Annotated[List[bytes],File()]):
    return {"file sizes":[len(Fl) for Fl in file]}
@app.post("/mul_file_upload/")
async def mult_file(files: list[UploadFile]):
    return {"file names":[file.filename for file in files]}
from fastapi.responses import HTMLResponse
@app.get("/html_dat/")
async def cont_data():

    content="""
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

@app.post("/upload_file_limit_size/")
async def upload_file_limit_size(file: UploadFile = File(..., max_length=10_000_000)):#limit size of file
    return {"filename": file.filename}


#Request Forms and Files----------

# Route to handle both form data and file uploads
@app.post("/submit_form_and_file/")
async def submit_form_and_file(username: str = Form(...),password: str = Form(...),profile_picture: UploadFile = File(...),):
    return {
        "username": username,
        "password": password,
        "file_name": profile_picture.filename,
    }

#Handling Errors--------------
#you can handle errors and return custom error responses using several mechanisms
#you would normally return an HTTP status code in the range of 400 (from 400 to 499).
#The status codes in the 400 range mean that there was an error from the client.
from fastapi import HTTPException
i={"foo":"sagarbhukya"}
@app.get('/handling error/{item_id}')
async def handling_errors(item_id:str):
    if item_id not in i:
        raise HTTPException(status_code=404,detail="item not found")
    return {"item_data":i[item_data]}
@app.get("/it/{item_id}")
async def read_item(item_id: int):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
#--Add custom headers
items = {"foo": "The Foo Wrestlers"}
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

#Custom Exception Handlers:
from fastapi.responses import JSONResponse
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

#Path Operation Configuration---------------*******
#you can configure various aspects of path operations (routes) using special parameters and decorators. Here are some common configurations for path operations:
#Response Status Code
from typing import Set
class respo_sts(BaseModel):
    name:str
    desc:Union[str,None]=None
    price:float
    tags:Set[str]=set()
@app.post("/response_stat/",response_model=respo_sts,status_code=status.HTTP_201_CREATED)
async def response_path_config(item:respo_sts):
    return item
#Tags
@app.post("/tags1/",response_model=respo_sts,tags=["tags"])
async def tags(item:respo_sts):
    return item
@app.post("/tgas1/",tags=["tags"])
async def tags1():
    return [{"name":"sagar","price":47}]
@app.post("/another_tag/",tags=["next tag"])
async def next_tags():
    return [{"mail":"sagarbhukya-08@gmail.xcom","pswd":"Sagar@123"}]
#Multiple Tags
@app.get("/multiple/", tags=["items", "apis"])
async def read_items():
    return {"message": "Read items"}
#Tags with Enums
#If you have a big application, you might end up accumulating several tags, and you would want to make sure you always use the same tag for related path operations.
from enum import Enum
class Tags(Enum):
    names="Names"
    sections="Sections"
@app.get("/names/",tags=[Tags.names])
async def tags_with_names():
    return ["sagar","prashganth"]
@app.get("/section",tags=[Tags.sections])
async def tags_with_section():
    return ["a","b","c"]
#Summary and description
@app.post(
    "/summary_description/",
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item:int):
    return item
#Response description
@app.post("/response_decsription/",summary="Hi dear",response_description="Hi my name is sagar")
async def respo_desccri(name:str):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return name
#Deprecate a path operation
@app.get("/a_/",tags=["Deprecate"])
async def depr(name:str):
    return name
@app.get("/_a_/",tags=["Deprecate"],deprecated=True)
async def depr_1(name:str):
    return name

#JSON Compatible Encoder-------------------
#In FastAPI, a JSON-compatible encoder is responsible for converting Python objects into JSON format. FastAPI uses the jsonable_encoder function from the fastapi.encoders module to perform this encoding.
from fastapi.encoders import jsonable_encoder
class db(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None
fake_db={}
@app.post('/json_encode/{id}')
async def json_en(id:int,item:db):
    json_compatible_item_data=jsonable_encoder(item)
    fake_db[id]=json_compatible_item_data
    return fake_db

#Body - Updates_____________________Later discuss
#In FastAPI, the Body class is used to define request bodies in route functions. When working with updates or modifications, you often use the Body class to receive data in the request body. The Body class allows you to specify additional information about the request body, such as whether it is required or whether it has a specific media type.


#Dependency______________________________________________________________________________________________
#In FastAPI, a dependency is a reusable component that can be used to perform some action or provide data that is required by one or more route functions. Dependencies are a way to organize and share common functionality among different parts of your application. They are typically used for tasks such as authentication, authorization, database connections, and more.
from fastapi import Depends
# Define a dependency function named common_parameters
async def common_parameters(
        q:Union[str,None]=None,skip:int=0,limit:int=100
):
    return {"q":q,"skip":skip,"limit":limit}
# Define a route that depends on the common_parameters function
@app.get("/dep/",tags=["Dependencies"])
async def depence(item:dict=Depends(common_parameters)):
    return item
#here calling another one with common_parameters
@app.get("/dep1/",tags=["Dependencies"])
async def depence(item:dict=Depends(common_parameters)):
    return item
#Share Annotated dependencies
CommonDep= Annotated [ dict,Depends(common_parameters)]
@app.get("/annotedDep/",tags=["Dependencies"])
async def anoted_dep(item:CommonDep):
    return item
@app.get("/annoteddep1/",tags=["Dependencies"])
async def annotedep1(item:CommonDep):
    return item

#Classes as Dependencies----
#creating a simple class
class Cat:
    def __init__(self, name: str):
        self.name = name
fluffy = Cat(name="Mr Fluffy")
#-------------
fake_items = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
class Common:
    def __init__(self,q:Union[str,None]=None,skip:int=0,limit:int=100):
        self.q=q
        self.skip=skip
        self.limit=limit
@app.get("/classdepen/",tags=["Dependencies"])
async def class_dep(common=Depends(Common)):
    response={}
    if common.q:
        response.update({"q":common.q})
    items=fake_items[common.skip:common.skip+common.limit]
    response.update({"items":items})
    return response

#Sub-dependencies------
## Dependency function query_extractor: Extracts the value of query parameter 'q'
def query_extractor(q: str | None = None):
    return q
# Extracts the value of query parameter 'q' using the query_extractor dependency
# If 'q' is not provided, it falls back to the value of the last_query cookie
def query_or_cookie_extractor(q:Annotated[str,Depends(query_extractor)],last_query:Annotated[str | None,Cookie()]=None):
    if not q:
        return last_query
    return q
# Route /items/: Depends on query_or_cookie_extractor to get the value of 'q' or the last_query cookie
@app.get("/sub_dep/",tags=["Dependencies"])
async def sub_depends(query_or_default:Annotated[str,Depends(query_or_cookie_extractor)]):
    return {"q_or_cookie":query_or_default}


#Dependencies in path operation decorators
# Dependency function verify_token: Validates the 'X-Token' header
async def verify_token(x_token:Annotated[str, Header()]):
    if x_token!="fake-super-secrer-token":
        raise HTTPException(status_code=400,detail="X-token header invalid")
# Dependency function verify_key: Validates and extracts the 'X-Key' header
async def verify_key(x_key:Annotated[str, Header()]):
    if x_key!="fake-super-secrer-key":
        raise HTTPException(status_code=400,detail="X-key header invalid")
    return x_key
# Route /items/: Depends on verify_token and verify_key
@app.get("/path_depnds/",dependencies=[Depends(verify_token),Depends(verify_key)],tags=["Dependencies"])
async def path_dep():
    return [{"item": "Foo"}, {"item": "Bar"}]

#Global Dependencies
# Create a FastAPI instance with global dependencies
ap = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
# Route /items/: Depends on verify_token and verify_key
@ap.get("/global1/",tags=["Dependencies"])
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]
# Route /users/: Depends on verify_token and verify_key
@ap.get("/global2/",tags=["Dependencies"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

#yeild with dependies---
from fastapi import HTTPException
# Sample data representing items with descriptions and owners
dat = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}
# Custom exception to represent an error related to ownership
class onwner(Exception):
    pass
def get_username():
    try:
        yield "Sagar"
    except onwner as e:
        # If an OwnerError occurs, raise an HTTPException with a 400 status code
        raise HTTPException(status_code=400,detail="owner error:{e}")
# Route /items/{item_id}
# Depends on the get_username dependency to get the username
@app.get("/yield_depends/{item_id}",tags=["Dependencies"])
def get_item(item_id:str, usernam:str=Depends(get_username)):
    # Check if the item_id is in the sample data
    if item_id not in dat:
        # If not found, raise an HTTPException with a 404 status code
        raise HTTPException(status_code=400,detail="Item not found")
    # Get the item details from the sample data
    item=dat[item_id]
    # Check if the owner of the item matches the retrieved username
    if item["owner"]!=usernam:
        # If not matching, raise a custom OwnerError
        raise onwner(usernam)
    # If everything is valid, return the item details
    return item