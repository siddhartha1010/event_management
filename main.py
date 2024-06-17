from fastapi import FastAPI,Request
from routes.userRoutes import userrouter
from routes.taskRoutes import taskrouter
from auth import authentication
from fastapi.responses import JSONResponse

app = FastAPI()
app.include_router(authentication.router)
app.include_router(userrouter)
app.include_router(taskrouter)