from datetime import datetime
from typing import TypedDict


class Ticket(TypedDict):
    id: int
    title: str
    description: str
    status: str
    created_at: str

