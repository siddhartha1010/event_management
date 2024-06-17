from models.taskModels import Task
from fastapi import APIRouter,Depends
from schema.taskSchemas import list_serail
from config.database import collection
from auth.oauth2 import oauth2_schema

taskrouter =APIRouter(
    prefix='/api/v1/task',
    tags=['task']
)

@taskrouter.post('/create')
async def create_task(task:Task):
    collection.insert_one(dict(task))


@taskrouter.get('/get')
async def get_task(token:str=Depends(oauth2_schema)):
    tasks = list_serail(collection.find())
    return list(tasks)




