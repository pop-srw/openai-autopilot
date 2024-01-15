from typing import List, Optional
from pydantic import BaseModel


class AutopilotMessage(BaseModel):
    role: str
    content: str


class AutopilotData(BaseModel):
    id: int
    messages: List[AutopilotMessage]
    response: Optional[str] = None


class AutopilotDataList(BaseModel):
    data_list: List[AutopilotData]
