from pydantic import BaseModel

class Employee(BaseModel):
    name:str
    email:str
    address:str
    photo:str
    phoneNumber:str
    experience:str
    
