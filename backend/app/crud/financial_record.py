from typing import List, Optional
from sqlmodel import Session, select
from app.models.financial_record import FinancialRecord


def create_record(db: Session, record: FinancialRecord) -> FinancialRecord:
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_record(db: Session, record_id: int) -> Optional[FinancialRecord]:
    return db.get(FinancialRecord, record_id)


def get_records(db: Session, skip: int = 0, limit: int = 100) -> List[FinancialRecord]:
    return db.exec(select(FinancialRecord).offset(skip).limit(limit)).all()


def update_record(
    db: Session, record_id: int, record: FinancialRecord
) -> Optional[FinancialRecord]:
    db_record = get_record(db, record_id)
    if db_record:
        for key, value in record.dict(exclude_unset=True).items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record


def delete_record(db: Session, record_id: int) -> bool:
    record = get_record(db, record_id)
    if record:
        db.delete(record)
        db.commit()
        return True
    return False
