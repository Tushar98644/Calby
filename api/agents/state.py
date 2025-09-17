from typing import TypedDict, NotRequired

class ConversationState(TypedDict):
    needs_transfer: bool
    transfer_reason: NotRequired[str]
    summary: NotRequired[str]