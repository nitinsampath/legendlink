from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    date_uploaded = Column(DateTime, default=lambda: datetime.now(UTC))
    type = Column(String)
    amount = Column(Integer)
