from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from datetime import datetime, timedelta
import os

from models import Student, Teacher, Book, Magazine, BorrowRecord, BorrowRequest, ReturnRequest
from database import get_collections
from xml_utils import export_to_xml, import_from_xml, validate_xml

app = FastAPI(title="Library Management System")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Library Management System API is running"}

# ==================== STUDENT ENDPOINTS ====================

@app.get("/api/library/{library_id}/students")
async def get_students(library_id: str):
    """Get all students from a library"""
    collections = get_collections(library_id)
    students = list(collections['students'].find({}, {'_id': 0}))
    return {"students": students}

@app.post("/api/library/{library_id}/students")
async def create_student(library_id: str, student: Student):
    """Create a new student - demonstrates Polymorphism (different from Teacher)"""
    collections = get_collections(library_id)
    student_dict = student.model_dump()
    collections['students'].insert_one(student_dict)
    # Remove MongoDB ObjectId before returning
    student_dict.pop('_id', None)
    return {"message": "Student created successfully", "student": student_dict}

@app.get("/api/library/{library_id}/students/{student_id}")
async def get_student(library_id: str, student_id: str):
    """Get a specific student"""
    collections = get_collections(library_id)
    student = collections['students'].find_one({"id": student_id}, {'_id': 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/api/library/{library_id}/students/{student_id}")
async def update_student(library_id: str, student_id: str, student: Student):
    """Update a student"""
    collections = get_collections(library_id)
    student_dict = student.model_dump()
    result = collections['students'].update_one({"id": student_id}, {"$set": student_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully", "student": student_dict}

@app.delete("/api/library/{library_id}/students/{student_id}")
async def delete_student(library_id: str, student_id: str):
    """Delete a student"""
    collections = get_collections(library_id)
    result = collections['students'].delete_one({"id": student_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

# ==================== TEACHER ENDPOINTS ====================

@app.get("/api/library/{library_id}/teachers")
async def get_teachers(library_id: str):
    """Get all teachers from a library"""
    collections = get_collections(library_id)
    teachers = list(collections['teachers'].find({}, {'_id': 0}))
    return {"teachers": teachers}

@app.post("/api/library/{library_id}/teachers")
async def create_teacher(library_id: str, teacher: Teacher):
    """Create a new teacher - demonstrates Polymorphism (different from Student)"""
    collections = get_collections(library_id)
    teacher_dict = teacher.model_dump()
    collections['teachers'].insert_one(teacher_dict)
    # Remove MongoDB ObjectId before returning
    teacher_dict.pop('_id', None)
    return {"message": "Teacher created successfully", "teacher": teacher_dict}

@app.get("/api/library/{library_id}/teachers/{teacher_id}")
async def get_teacher(library_id: str, teacher_id: str):
    """Get a specific teacher"""
    collections = get_collections(library_id)
    teacher = collections['teachers'].find_one({"id": teacher_id}, {'_id': 0})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.put("/api/library/{library_id}/teachers/{teacher_id}")
async def update_teacher(library_id: str, teacher_id: str, teacher: Teacher):
    """Update a teacher"""
    collections = get_collections(library_id)
    teacher_dict = teacher.model_dump()
    result = collections['teachers'].update_one({"id": teacher_id}, {"$set": teacher_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher updated successfully", "teacher": teacher_dict}

@app.delete("/api/library/{library_id}/teachers/{teacher_id}")
async def delete_teacher(library_id: str, teacher_id: str):
    """Delete a teacher"""
    collections = get_collections(library_id)
    result = collections['teachers'].delete_one({"id": teacher_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted successfully"}

# ==================== BOOK ENDPOINTS ====================

@app.get("/api/library/{library_id}/books")
async def get_books(library_id: str):
    """Get all books from a library"""
    collections = get_collections(library_id)
    books = list(collections['books'].find({}, {'_id': 0}))
    return {"books": books}

@app.post("/api/library/{library_id}/books")
async def create_book(library_id: str, book: Book):
    """Create a new book - demonstrates Polymorphism (different from Magazine)"""
    collections = get_collections(library_id)
    book_dict = book.model_dump()
    collections['books'].insert_one(book_dict)
    # Remove MongoDB ObjectId before returning
    book_dict.pop('_id', None)
    return {"message": "Book created successfully", "book": book_dict}

@app.get("/api/library/{library_id}/books/{book_id}")
async def get_book(library_id: str, book_id: str):
    """Get a specific book"""
    collections = get_collections(library_id)
    book = collections['books'].find_one({"id": book_id}, {'_id': 0})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/api/library/{library_id}/books/{book_id}")
async def update_book(library_id: str, book_id: str, book: Book):
    """Update a book"""
    collections = get_collections(library_id)
    book_dict = book.model_dump()
    result = collections['books'].update_one({"id": book_id}, {"$set": book_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book updated successfully", "book": book_dict}

@app.delete("/api/library/{library_id}/books/{book_id}")
async def delete_book(library_id: str, book_id: str):
    """Delete a book"""
    collections = get_collections(library_id)
    result = collections['books'].delete_one({"id": book_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# ==================== MAGAZINE ENDPOINTS ====================

@app.get("/api/library/{library_id}/magazines")
async def get_magazines(library_id: str):
    """Get all magazines from a library"""
    collections = get_collections(library_id)
    magazines = list(collections['magazines'].find({}, {'_id': 0}))
    return {"magazines": magazines}

@app.post("/api/library/{library_id}/magazines")
async def create_magazine(library_id: str, magazine: Magazine):
    """Create a new magazine - demonstrates Polymorphism (different from Book)"""
    collections = get_collections(library_id)
    magazine_dict = magazine.model_dump()
    collections['magazines'].insert_one(magazine_dict)
    # Remove MongoDB ObjectId before returning
    magazine_dict.pop('_id', None)
    return {"message": "Magazine created successfully", "magazine": magazine_dict}

@app.get("/api/library/{library_id}/magazines/{magazine_id}")
async def get_magazine(library_id: str, magazine_id: str):
    """Get a specific magazine"""
    collections = get_collections(library_id)
    magazine = collections['magazines'].find_one({"id": magazine_id}, {'_id': 0})
    if not magazine:
        raise HTTPException(status_code=404, detail="Magazine not found")
    return magazine

@app.put("/api/library/{library_id}/magazines/{magazine_id}")
async def update_magazine(library_id: str, magazine_id: str, magazine: Magazine):
    """Update a magazine"""
    collections = get_collections(library_id)
    magazine_dict = magazine.model_dump()
    result = collections['magazines'].update_one({"id": magazine_id}, {"$set": magazine_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Magazine not found")
    return {"message": "Magazine updated successfully", "magazine": magazine_dict}

@app.delete("/api/library/{library_id}/magazines/{magazine_id}")
async def delete_magazine(library_id: str, magazine_id: str):
    """Delete a magazine"""
    collections = get_collections(library_id)
    result = collections['magazines'].delete_one({"id": magazine_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Magazine not found")
    return {"message": "Magazine deleted successfully"}

# ==================== BORROW/RETURN OPERATIONS ====================

@app.post("/api/library/{library_id}/borrow")
async def borrow_item(library_id: str, request: BorrowRequest):
    """Borrow an item - demonstrates Polymorphism (different rules for students/teachers)"""
    collections = get_collections(library_id)
    
    # Check if item exists and is available
    item = collections['books'].find_one({"id": request.item_id}, {'_id': 0})
    item_type = "book"
    if not item:
        item = collections['magazines'].find_one({"id": request.item_id}, {'_id': 0})
        item_type = "magazine"
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if not item['available']:
        raise HTTPException(status_code=400, detail="Item is not available")
    
    # Check if person exists
    person = collections['students'].find_one({"id": request.person_id}, {'_id': 0})
    person_type = "student"
    if not person:
        person = collections['teachers'].find_one({"id": request.person_id}, {'_id': 0})
        person_type = "teacher"
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Check borrow limit (Polymorphism: different limits for students vs teachers)
    active_borrows = collections['borrow_records'].count_documents({
        "person_id": request.person_id,
        "status": "borrowed"
    })
    
    max_limit = person.get('max_borrow_limit', 5)
    if active_borrows >= max_limit:
        raise HTTPException(status_code=400, detail=f"Borrow limit reached ({max_limit} items)")
    
    # Create borrow record
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    borrow_record = BorrowRecord(
        person_id=request.person_id,
        person_name=person['name'],
        person_type=person_type,
        item_id=request.item_id,
        item_title=item['title'],
        item_type=item_type,
        borrow_date=borrow_date,
        due_date=due_date,
        status="borrowed"
    )
    
    # Update item availability
    if item_type == "book":
        collections['books'].update_one({"id": request.item_id}, {"$set": {"available": False}})
    else:
        collections['magazines'].update_one({"id": request.item_id}, {"$set": {"available": False}})
    
    # Insert borrow record
    collections['borrow_records'].insert_one(borrow_record.model_dump())
    
    return {"message": "Item borrowed successfully", "record": borrow_record.model_dump()}

@app.post("/api/library/{library_id}/return")
async def return_item(library_id: str, request: ReturnRequest):
    """Return an item"""
    collections = get_collections(library_id)
    
    # Find borrow record
    record = collections['borrow_records'].find_one({"id": request.record_id}, {'_id': 0})
    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    if record['status'] != "borrowed":
        raise HTTPException(status_code=400, detail="Item already returned")
    
    # Update borrow record
    return_date = datetime.now().strftime("%Y-%m-%d")
    collections['borrow_records'].update_one(
        {"id": request.record_id},
        {"$set": {"status": "returned", "return_date": return_date}}
    )
    
    # Update item availability
    if record['item_type'] == "book":
        collections['books'].update_one({"id": record['item_id']}, {"$set": {"available": True}})
    else:
        collections['magazines'].update_one({"id": record['item_id']}, {"$set": {"available": True}})
    
    return {"message": "Item returned successfully"}

@app.get("/api/library/{library_id}/borrow-records")
async def get_borrow_records(library_id: str):
    """Get all borrow records"""
    collections = get_collections(library_id)
    records = list(collections['borrow_records'].find({}, {'_id': 0}))
    
    # Check for overdue items
    today = datetime.now().strftime("%Y-%m-%d")
    for record in records:
        if record['status'] == 'borrowed' and record['due_date'] < today:
            record['status'] = 'overdue'
            collections['borrow_records'].update_one(
                {"id": record['id']},
                {"$set": {"status": "overdue"}}
            )
    
    return {"records": records}

@app.get("/api/library/{library_id}/search")
async def search_library(library_id: str, query: str = ""):
    """Search for items or people in the library"""
    collections = get_collections(library_id)
    
    query_lower = query.lower()
    
    # Search books
    books = list(collections['books'].find({}, {'_id': 0}))
    matched_books = [b for b in books if query_lower in b['title'].lower() or query_lower in b['author'].lower()]
    
    # Search magazines
    magazines = list(collections['magazines'].find({}, {'_id': 0}))
    matched_magazines = [m for m in magazines if query_lower in m['title'].lower() or query_lower in m['author'].lower()]
    
    # Search students
    students = list(collections['students'].find({}, {'_id': 0}))
    matched_students = [s for s in students if query_lower in s['name'].lower()]
    
    # Search teachers
    teachers = list(collections['teachers'].find({}, {'_id': 0}))
    matched_teachers = [t for t in teachers if query_lower in t['name'].lower()]
    
    return {
        "books": matched_books,
        "magazines": matched_magazines,
        "students": matched_students,
        "teachers": matched_teachers
    }

# ==================== XML OPERATIONS ====================

@app.get("/api/library/{library_id}/xml/export")
async def export_library_xml(library_id: str):
    """Export library data to XML format"""
    collections = get_collections(library_id)
    
    data = {
        'books': list(collections['books'].find({}, {'_id': 0})),
        'magazines': list(collections['magazines'].find({}, {'_id': 0})),
        'students': list(collections['students'].find({}, {'_id': 0})),
        'teachers': list(collections['teachers'].find({}, {'_id': 0}))
    }
    
    xml_string = export_to_xml(library_id, data)
    return {"xml": xml_string, "library_id": library_id}

@app.post("/api/library/{library_id}/xml/import")
async def import_library_xml(library_id: str, xml_data: Dict = Body(...)):
    """Import library data from XML format"""
    xml_string = xml_data.get('xml', '')
    
    if not validate_xml(xml_string):
        raise HTTPException(status_code=400, detail="Invalid XML format")
    
    try:
        data = import_from_xml(xml_string)
        collections = get_collections(library_id)
        
        # Import books
        for book in data['books']:
            collections['books'].update_one(
                {"id": book['id']},
                {"$set": book},
                upsert=True
            )
        
        # Import magazines
        for magazine in data['magazines']:
            collections['magazines'].update_one(
                {"id": magazine['id']},
                {"$set": magazine},
                upsert=True
            )
        
        # Import students
        for student in data['students']:
            collections['students'].update_one(
                {"id": student['id']},
                {"$set": student},
                upsert=True
            )
        
        # Import teachers
        for teacher in data['teachers']:
            collections['teachers'].update_one(
                {"id": teacher['id']},
                {"$set": teacher},
                upsert=True
            )
        
        return {
            "message": "XML imported successfully",
            "imported": {
                "books": len(data['books']),
                "magazines": len(data['magazines']),
                "students": len(data['students']),
                "teachers": len(data['teachers'])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error importing XML: {str(e)}")

@app.post("/api/library/xml/sync")
async def sync_libraries(sync_data: Dict = Body(...)):
    """Sync data between Library A and Library B"""
    source_library = sync_data.get('source', 'a')
    target_library = sync_data.get('target', 'b')
    
    if source_library not in ['a', 'b'] or target_library not in ['a', 'b']:
        raise HTTPException(status_code=400, detail="Invalid library IDs")
    
    if source_library == target_library:
        raise HTTPException(status_code=400, detail="Source and target libraries must be different")
    
    # Export from source
    source_collections = get_collections(source_library)
    data = {
        'books': list(source_collections['books'].find({}, {'_id': 0})),
        'magazines': list(source_collections['magazines'].find({}, {'_id': 0})),
        'students': list(source_collections['students'].find({}, {'_id': 0})),
        'teachers': list(source_collections['teachers'].find({}, {'_id': 0}))
    }
    
    # Import to target
    target_collections = get_collections(target_library)
    
    for book in data['books']:
        target_collections['books'].update_one(
            {"id": book['id']},
            {"$set": book},
            upsert=True
        )
    
    for magazine in data['magazines']:
        target_collections['magazines'].update_one(
            {"id": magazine['id']},
            {"$set": magazine},
            upsert=True
        )
    
    for student in data['students']:
        target_collections['students'].update_one(
            {"id": student['id']},
            {"$set": student},
            upsert=True
        )
    
    for teacher in data['teachers']:
        target_collections['teachers'].update_one(
            {"id": teacher['id']},
            {"$set": teacher},
            upsert=True
        )
    
    return {
        "message": f"Successfully synced Library {source_library.upper()} to Library {target_library.upper()}",
        "synced": {
            "books": len(data['books']),
            "magazines": len(data['magazines']),
            "students": len(data['students']),
            "teachers": len(data['teachers'])
        }
    }

@app.get("/api/library/{library_id}/stats")
async def get_library_stats(library_id: str):
    """Get statistics for a library"""
    collections = get_collections(library_id)
    
    stats = {
        "total_books": collections['books'].count_documents({}),
        "available_books": collections['books'].count_documents({"available": True}),
        "total_magazines": collections['magazines'].count_documents({}),
        "available_magazines": collections['magazines'].count_documents({"available": True}),
        "total_students": collections['students'].count_documents({}),
        "total_teachers": collections['teachers'].count_documents({}),
        "active_borrows": collections['borrow_records'].count_documents({"status": "borrowed"}),
        "overdue_items": collections['borrow_records'].count_documents({"status": "overdue"})
    }
    
    return stats

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
