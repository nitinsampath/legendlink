from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class File(BaseModel):
    id: str
    name: str
    upload_date: datetime
    type: Literal["Invoice", "Purchase Order"]