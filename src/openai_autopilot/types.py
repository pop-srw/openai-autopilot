from typing import List, Optional
from enum import Enum
from pydantic import BaseModel


class AutopilotRoleEnum(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class AutopilotMessage(BaseModel):
    role: AutopilotRoleEnum
    content: str


class AutopilotData(BaseModel):
    id: int
    messages: List[AutopilotMessage]
    response: Optional[str] = None


class AutopilotDataList(BaseModel):
    data_list: List[AutopilotData]
