from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta ,timezone
from jose import jwt,JWTError

from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from config.database import token_collection,collection_name
from schema.userSchemas import list_serail, individual_serial
from routes.hash import Hash
from auth import oauth2
from pydantic import BaseModel,EmailStr



router = APIRouter(
    tags=['authentication']
)



# @router.post('/token')
# def get_token(request:OAuth2PasswordRequestForm=Depends()):
#     # user = individual_serial(collection_name.find())
#     user = collection_name.find_one({"email": request.username})
#     print(user)
#     if not user:
#         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email address")
#     # if not Hash.verify(user.password, request.password):
#     print(request.password)
#     print(user["password"])
#     if not Hash().verify(user["password"], request.password):
#         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
#     access_token = oauth2.create_access_token(data={'sub':user["email"]})

#     return {'access_token': access_token, 'token_type': 'bearer','email':user["email"]}

class TokenRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

    
# @router.post('/token')
# async def get_token(request: TokenRequest):
#     user = collection_name.find_one({"email": request.email})
#     print(user)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email address")
#     print(request.password)
#     print(user["password"])
#     if not Hash().verify(user["password"], request.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
#     access_token = oauth2.create_access_token(data={'sub': user["email"]})

#     return {'access_token': access_token, 'token_type': 'bearer', 'email': user["email"]}
@router.post('/token')
async def get_token(request: TokenRequest):
    user = collection_name.find_one({"email": request.email})
    if not user or not Hash().verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password")

    access_token = oauth2.create_access_token(data={'sub': user["email"] ,'role':user["role"]})
    refresh_token = oauth2.create_refresh_token(data={'sub': user["email"],'role':user["role"]})
    
    
    nepal_offset = timedelta(hours=5, minutes=45)
    nepal_timezone = timezone(nepal_offset)

    expires_at_datetime = datetime.now(nepal_timezone) + timedelta(days=1)
    expires_at_readable = expires_at_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')


    token_data = {
        "email": user["email"],
        "token": refresh_token,
        # "expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).timestamp()
        "expires_at":expires_at_readable
    }
    token_collection.insert_one(token_data)
    print("The  token_data is",token_data)

    response = JSONResponse(content={
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'email': user["email"]
    })
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True  
    )

    return response


@router.post('/refresh')
async def refresh_token(request: RefreshTokenRequest):
    refresh_token = request.refresh_token#yo user ko req garda aako
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    db_token = token_collection.find_one({"token": refresh_token})
    # print("The token is",db_token)
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    nepal_offset = timedelta(hours=5, minutes=45)
    nepal_timezone = timezone(nepal_offset)
    current_time = datetime.now(nepal_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')

    if db_token["expires_at"] < current_time:
        token_collection.delete_one({"token": refresh_token})
        raise HTTPException(status_code=401, detail="Expired refresh token")

    try:
        payload = jwt.decode(refresh_token, oauth2.SECRET_KEY, algorithms=[oauth2.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = oauth2.create_access_token(data={"sub": payload["sub"]}, expires_delta=timedelta(minutes=15))
    new_refresh_token = oauth2.create_refresh_token(data={"sub": payload["sub"]}, expires_delta=timedelta(days=1))

    expires_at_datetime = datetime.now(nepal_timezone) + timedelta(days=1)
    expires_at_readable = expires_at_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')

    token_collection.update_one(
        {"token": refresh_token},
        {"$set": {
            "token": new_refresh_token,
            "expires_at": expires_at_readable
        }}
    )

    response = JSONResponse(content={"access_token": new_access_token})
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True
    )

    return response

# from bson import ObjectId

# @router.post('/token')
# async def get_token(request: OAuth2PasswordRequestForm = Depends()):
#     # Retrieve the user from the MongoDB collection based on the provided username
#     user = await collection_name.find_one({"username": request.username})
    
#     # Check if the user exists
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid credentials"
#         )

#     # Perform the password verification
#     if not Hash.verify(user["password"], request.password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Incorrect password"
#         )

#     # If everything is correct, create and return the access token
#     access_token = oauth2.create_access_token(data={'sub': str(user['_id'])})
#     return {'access_token': access_token, 'token_type': 'bearer', 'user_id': str(user['_id'])}

# @router.post('/token')
# async def get_token(request: OAuth2PasswordRequestForm = Depends()):
#     # Retrieve the user from the MongoDB collection
#     # user_list = individual_serial(collection_name.find())
#     # print(user_list)
#     user = collection_name.find_one({"name": request.username})
#     print(user)
    
    
#     # Check if any user exists
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid credentials"
#         )

#     # For simplicity, let's assume the first user is the one you're interested in
#     # user = user_list[0]
#     # print("The user is",user)

#     # Perform the password verification
#     if not Hash.verify(request.password, user["password"]):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Incorrect password"
#         )

#     # If everything is correct, create and return the access token
#     access_token = oauth2.create_access_token(data={'sub': user['name']})
#     return {'access_token': access_token, 'token_type': 'bearer', 'username': user['name']}

# @router.post('/token')
# async def get_token(request: OAuth2PasswordRequestForm = Depends()):
#     # Retrieve the user from the MongoDB collection
#     user = await collection_name.find_one({"username": request.username})
    
#     # If user does not exist, raise HTTP 404
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid credentials"
#         )

#     # Initialize Hash class
#     hasher = Hash()

#     # Verify password
#     if not hasher.verify(user['password'], request.password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Incorrect password"
#         )

#     # If everything is correct, create and return the access token
#     access_token = oauth2.create_access_token(data={'sub': user['username']})
#     return {'access_token': access_token, 'token_type': 'bearer', 'username': user['username']}
