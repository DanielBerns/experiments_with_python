from datetimes import datetime, UTC
from pydantic import BaseModel

class Node(BaseModel):
    uri: str
    context: str

class Edge(BaseModel):
    left_node_id: int
    right_node_id: int

class Attribute(BaseModel):
    uri: str
    context: str
    key: str

class SerializedValue(BaseModel):
    kind: str
    content: str

a_node = Node(
    uri = "/thing/fruit",
    context = "A thing you can eat"
)

other_node = Node(
    uri = "/property/color")
    context = "It is a property of things"

an_edge = Edge(
    left_node_id: 1,
    right_node_id: 2,
    uri: "/relationship"
)
print(a_node)
print(other_node)
