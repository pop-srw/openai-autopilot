from typing import TypedDict, List, Optional


class Message(TypedDict):
    role: str
    content: str


class DataItem(TypedDict, total=False):  # total=False makes all keys optional
    id: int
    messages: List[Message]
    response: Optional[str]  # response is optional and can be a string


DataListType = List[DataItem]
