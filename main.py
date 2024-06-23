from fastapi import FastAPI,Request
from routes.userRoutes import userrouter
from routes.taskRoutes import taskrouter
from routes import employeeRoutes
from auth import authentication
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)
app.include_router(authentication.router)
app.include_router(userrouter)
app.include_router(taskrouter)
app.include_router(employeeRoutes.router)
