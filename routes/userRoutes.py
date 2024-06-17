from routes.hash import Hash
from fastapi import APIRouter,status,HTTPException

from models.userModel import User#Basic format of how todo will look like

from config.database import collection_name#name of collection
from schema.userSchemas import list_serail,individual_serial
from bson import ObjectId


userrouter =APIRouter(
    prefix='/api/v1/users',
    tags=['user']
)

@userrouter.post("/create")
async def create_user(user:User):
     if user.password !=user.passwordConfirm:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Passwords do not match") 
     existing_user = collection_name.find_one({"email": user.email})
     if existing_user:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Email already registered"
        )
     hasher =Hash()
     user_data = {
        "name": user.name,
        "email": user.email,
        "password": hasher.bcrypt(user.password),
        "role": user.role
        # "passwordConfirm": user.passwordConfirm
    }
    
     collection_name.insert_one(dict(user_data))
     return {"message":"User created successfully"}

