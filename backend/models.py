from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# Base Classes demonstrating Encapsulation

class Person(BaseModel):
    """Base class for all people in the library system"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: str
    person_type: str  # 'student' or 'teacher'
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "123-456-7890"
            }
        }

class Student(Person):
    """Student class inheriting from Person - demonstrates Inheritance"""
    student_id: str
    grade_level: str
    max_borrow_limit: int = 5
    person_type: str = "student"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice Johnson",
                "email": "alice@school.com",
                "phone": "123-456-7890",
                "student_id": "S001",
                "grade_level": "10th"
            }
        }

class Teacher(Person):
    """Teacher class inheriting from Person - demonstrates Inheritance"""
    teacher_id: str
    department: str
    max_borrow_limit: int = 10
    person_type: str = "teacher"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dr. Smith",
                "email": "smith@school.com",
                "phone": "123-456-7891",
                "teacher_id": "T001",
                "department": "Computer Science"
            }
        }

class Item(BaseModel):
    """Base class for all items in the library"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    author: str
    isbn: str
    available: bool = True
    item_type: str  # 'book' or 'magazine'
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample Book",
                "author": "Author Name",
                "isbn": "978-0131234456"
            }
        }

class Book(Item):
    """Book class inheriting from Item - demonstrates Inheritance"""
    genre: str
    pages: int
    publisher: str
    item_type: str = "book"
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Object-Oriented Design",
                "author": "Martin Fowler",
                "isbn": "978-0131234456",
                "genre": "Computer Science",
                "pages": 450,
                "publisher": "Addison-Wesley"
            }
        }

class Magazine(Item):
    """Magazine class inheriting from Item - demonstrates Inheritance"""
    issue_number: str
    publication_month: str
    item_type: str = "magazine"
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Tech Monthly",
                "author": "Various",
                "isbn": "MAG-001",
                "issue_number": "42",
                "publication_month": "January 2024"
            }
        }

class BorrowRecord(BaseModel):
    """Represents a borrowing transaction - demonstrates Composition"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    person_id: str
    person_name: str
    person_type: str
    item_id: str
    item_title: str
    item_type: str
    borrow_date: str
    due_date: str
    return_date: Optional[str] = None
    status: str = "borrowed"  # 'borrowed', 'returned', 'overdue'
    
    class Config:
        json_schema_extra = {
            "example": {
                "person_id": "uuid-person",
                "person_name": "Alice Johnson",
                "person_type": "student",
                "item_id": "uuid-item",
                "item_title": "Object-Oriented Design",
                "item_type": "book",
                "borrow_date": "2024-01-01",
                "due_date": "2024-01-15",
                "status": "borrowed"
            }
        }

class BorrowRequest(BaseModel):
    person_id: str
    item_id: str
    
class ReturnRequest(BaseModel):
    record_id: str