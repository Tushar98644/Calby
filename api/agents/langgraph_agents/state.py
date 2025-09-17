from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages, AnyMessage

class ConversationState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]