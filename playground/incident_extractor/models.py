from typing import Literal
from pydantic import BaseModel

class Incident(BaseModel):

    pipeline: str
    status: Literal['SUCCESS', 'FAILED', 'RUNNING']
    failed_task: str | None = None
    error_type: str | None = None
    evidence: list[str]
    missing_information: list[str]