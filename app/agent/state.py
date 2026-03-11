from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict):
    question: str
    country: Optional[str]
    fields: Optional[List[str]]
    api_data: Optional[Dict[str, Any]]
    answer: Optional[str]
    error: Optional[str]