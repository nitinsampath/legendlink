from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field


class FinancialRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date_uploaded: datetime = Field(default_factory=lambda: datetime.now(UTC))
    type: str
    amount: int
