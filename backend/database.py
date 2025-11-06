from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')

client = MongoClient(MONGO_URL)
db = client.library_management

# Collections for Library A
library_a_students = db.library_a_students
library_a_teachers = db.library_a_teachers
library_a_books = db.library_a_books
library_a_magazines = db.library_a_magazines
library_a_borrow_records = db.library_a_borrow_records

# Collections for Library B
library_b_students = db.library_b_students
library_b_teachers = db.library_b_teachers
library_b_books = db.library_b_books
library_b_magazines = db.library_b_magazines
library_b_borrow_records = db.library_b_borrow_records

def get_collections(library_id: str):
    """Get collections for a specific library"""
    if library_id == 'a':
        return {
            'students': library_a_students,
            'teachers': library_a_teachers,
            'books': library_a_books,
            'magazines': library_a_magazines,
            'borrow_records': library_a_borrow_records
        }
    elif library_id == 'b':
        return {
            'students': library_b_students,
            'teachers': library_b_teachers,
            'books': library_b_books,
            'magazines': library_b_magazines,
            'borrow_records': library_b_borrow_records
        }
    else:
        raise ValueError(f"Invalid library_id: {library_id}")