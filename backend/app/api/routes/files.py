from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db import get_session
from app.crud.financial_record import create_record
from app.models.financial_record import FinancialRecord
from pydantic import BaseModel
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.indices import VectorStoreIndex
import tempfile
import os

router = APIRouter()


async def parse_pdf_content(pdf_content: bytes) -> tuple[str, float]:
    # Create a temporary file to store the PDF content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_content)
        tmp_path = tmp_file.name

    try:
        # Load the PDF using LlamaIndex
        documents = SimpleDirectoryReader(input_files=[tmp_path]).load_data()

        # Create an index from the document
        index = VectorStoreIndex.from_documents(documents)

        # Create a query engine
        query_engine = index.as_query_engine()

        # Query to determine document type
        type_response = query_engine.query(
            "Is this document an invoice or a purchase order? Just respond with either 'invoice' or 'purchase_order'."
        )
        doc_type = str(type_response).lower().strip()

        # Query to extract the total amount
        amount_response = query_engine.query(
            "What is the total amount in this document? Please respond with just the number. Please convert the dollar amount into cents. For example $252.52 should be 25252"
        )
        # Extract numeric value from response
        amount = float(
            "".join(filter(lambda x: x.isdigit() or x == ".", str(amount_response)))
        )

        if doc_type not in ["invoice", "purchase_order"]:
            raise ValueError("Could not determine document type")

        return doc_type, amount

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_session),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        # Read the PDF content
        pdf_content = await file.read()

        # Parse the PDF to determine type and amount
        doc_type, amount = await parse_pdf_content(pdf_content)

        # Create the financial record
        record = FinancialRecord(
            file_name=file.filename,
            type=doc_type,
            amount=amount,
        )

        db_record = create_record(db, record)

        return {
            "file_name": db_record.file_name,
            "record_id": db_record.id,
            "type": db_record.type,
            "amount": db_record.amount,
            "date_uploaded": db_record.date_uploaded,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
