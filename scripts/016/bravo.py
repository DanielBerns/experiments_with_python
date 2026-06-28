from pydantic import BaseModel

class Node(BaseModel):
    identifier: int
    parent_identifier: int
    author_identifier: int
    uri: str
    title: str
    content: str
    created_at: datetime

class Tag(BaseModel):
    identifier: int
    uri: str
    title: str
