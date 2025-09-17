from typing import TypedDict, NotRequired

class AgentState(TypedDict):
    transcript: str
    summary: NotRequired[str]