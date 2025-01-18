from fastapi import APIRouter, UploadFile
from typing import Dict

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile) -> Dict[str, str]:
    """
    Upload metadata of file to the database
    """
    # TODO set up DB and SQLModel
    return {"message": "File uploaded successfully"}
