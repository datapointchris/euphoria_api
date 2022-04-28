from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel


class TaskOut(BaseModel):
    id: int
    name: str
    category: str
    priority: int
    add_date: datetime
    complete_date: datetime | None


class TaskCreate(BaseModel):
    name: str
    category: str
    priority: int


