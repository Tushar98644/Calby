from typing import TypedDict, NotRequired

class ConversationState(TypedDict):
    transcript: str
    needs_transfer: bool
    summary: NotRequired[str]