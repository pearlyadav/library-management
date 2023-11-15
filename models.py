from pydantic import BaseModel
from datetime import datetime

class Student(BaseModel):
    name: str
    id: int
    school: str | None = None
    num_books_issued: int = 0
    has_currently_issued_book: bool = False
    date_added: datetime | None = None
    date_updated: datetime | None = None

class Book(BaseModel):
    name: str
    author: str
    num_issued: int = 0
    date_added: datetime | None = None
    date_updated: datetime | None = None