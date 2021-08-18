from typing import Optional, TypedDict


class MatchedGroup(TypedDict):
    min: str
    max: Optional[str]
    width_prop: str
    data_prop: str
    comment: str
