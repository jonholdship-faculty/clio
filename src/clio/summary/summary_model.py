from datetime import datetime
from pydantic import BaseModel


class ApplicationSummary(BaseModel):
    id: int
    date: datetime
    outcome: str
    reason: str
