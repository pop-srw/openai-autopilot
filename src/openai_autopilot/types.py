from typing import TypedDict, List, Optional


class AutopilotMessage(TypedDict):
    role: str
    content: str


AutopilotMessageType = List[AutopilotMessage]


class AutopilotData(TypedDict):
    id: int
    messages: AutopilotMessageType
    response: Optional[str]


AutopilotDataListType = List[AutopilotData]
