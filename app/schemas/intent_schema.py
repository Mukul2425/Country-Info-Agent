from pydantic import BaseModel
from typing import List


class IntentSchema(BaseModel):
    country: str
    fields: List[str]