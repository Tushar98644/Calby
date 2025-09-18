from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages, AnyMessage
from langgraph.graph.state import NotRequired

class ConversationState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    needs_transfer: bool
    summary: NotRequired[str]