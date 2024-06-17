from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from config.database import collection_name
from schema.userSchemas import list_serail, individual_serial
from routes.hash import Hash
from auth import oauth2



router = APIRouter(
    tags=['authentication']
)



@router.post('/token')
def get_token(request:OAuth2PasswordRequestForm=Depends()):
    # user = individual_serial(collection_name.find())
    user = collection_name.find_one({"email": request.username})
    print(user)
    if not user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email address")
    # if not Hash.verify(user.password, request.password):
    print(request.password)
    print(user["password"])
    if not Hash().verify(user["password"], request.password):
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    access_token = oauth2.create_access_token(data={'sub':user["email"]})

    return {'access_token': access_token, 'token_type': 'bearer','email':user["email"]}





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
