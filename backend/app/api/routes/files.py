from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_session
from app.crud.financial_record import create_record
from app.models.financial_record import FinancialRecord
from pydantic import BaseModel

router = APIRouter()


class FileUpload(BaseModel):
    file_name: str


@router.post("/upload")
async def upload_file(
    file_data: FileUpload,  # Changed to accept request body
    db: Session = Depends(get_session),
):
    record = FinancialRecord(
        file_name=file_data.file_name,  # Use the file_name from request
        type="upload",
        amount=1000,
    )

    db_record = create_record(db, record)

    return {
        "file_name": db_record.file_name,
        "record_id": db_record.id,
        "type": db_record.type,
        "amount": db_record.amount,
        "date_uploaded": db_record.date_uploaded,
    }
