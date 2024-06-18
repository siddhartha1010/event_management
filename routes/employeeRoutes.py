import os
from models.employeModels import Employee
from fastapi import APIRouter, UploadFile, HTTPException
from schema.employeeSchemas import list_serail
from config.database import employee_collection
from auth.oauth2 import oauth2_schema
from datetime import datetime
router =APIRouter(
    prefix='/api/v1/employee',
    tags=['employee']
)
UPLOAD_DIRECTORY='./img'

# @router.post('/img/upload')
@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        contents = await file.read()
        current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
        unique_filename = f"{current_time}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(contents)

        data_to_insert = {
            "filename": unique_filename,
            # "file_path": file_path,
            "upload_timestamp": datetime.now(),
        }

        employee_collection.insert_one(data_to_insert)
        

        return {"file_path": file_path, "filename": unique_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))