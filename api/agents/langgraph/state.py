from typing import TypedDict, NotRequired

class ConversationState(TypedDict):
    needs_transfer: bool
    summary: NotRequired[str]
    response: str