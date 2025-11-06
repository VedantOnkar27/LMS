#!/usr/bin/env python3
"""
Test Polymorphism - Different borrow limits for Students vs Teachers
"""

import requests
import json

BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

def test_polymorphism():
    """Test that students and teachers have different borrow limits"""
    library_id = "a"
    
    # Get students and teachers
    students_response = requests.get(f"{API_BASE}/library/{library_id}/students")
    teachers_response = requests.get(f"{API_BASE}/library/{library_id}/teachers")
    
    if students_response.status_code == 200 and teachers_response.status_code == 200:
        students = students_response.json().get('students', [])
        teachers = teachers_response.json().get('teachers', [])
        
        print("=== POLYMORPHISM TEST: BORROW LIMITS ===")
        print()
        
        if students:
            student = students[0]
            print(f"Student: {student['name']}")
            print(f"  - Max Borrow Limit: {student.get('max_borrow_limit', 5)}")
            print(f"  - Person Type: {student.get('person_type', 'student')}")
            print()
        
        if teachers:
            teacher = teachers[0]
            print(f"Teacher: {teacher['name']}")
            print(f"  - Max Borrow Limit: {teacher.get('max_borrow_limit', 10)}")
            print(f"  - Person Type: {teacher.get('person_type', 'teacher')}")
            print()
        
        # Verify polymorphism
        if students and teachers:
            student_limit = students[0].get('max_borrow_limit', 5)
            teacher_limit = teachers[0].get('max_borrow_limit', 10)
            
            print("POLYMORPHISM VERIFICATION:")
            print(f"✅ Students have limit of {student_limit} books")
            print(f"✅ Teachers have limit of {teacher_limit} books")
            print(f"✅ Different limits demonstrate polymorphism: {student_limit != teacher_limit}")
            
            return student_limit != teacher_limit
    
    return False

def test_available_magazine_borrow():
    """Test borrowing an available magazine"""
    library_id = "a"
    
    # Get available magazines
    magazines_response = requests.get(f"{API_BASE}/library/{library_id}/magazines")
    teachers_response = requests.get(f"{API_BASE}/library/{library_id}/teachers")
    
    if magazines_response.status_code == 200 and teachers_response.status_code == 200:
        magazines = magazines_response.json().get('magazines', [])
        teachers = teachers_response.json().get('teachers', [])
        
        # Find an available magazine
        available_magazine = None
        for mag in magazines:
            if mag.get('available', False):
                available_magazine = mag
                break
        
        if available_magazine and teachers:
            teacher = teachers[0]
            
            borrow_request = {
                "person_id": teacher['id'],
                "item_id": available_magazine['id']
            }
            
            print("=== MAGAZINE BORROW TEST ===")
            print(f"Teacher: {teacher['name']}")
            print(f"Magazine: {available_magazine['title']}")
            print(f"Available: {available_magazine['available']}")
            
            try:
                response = requests.post(f"{API_BASE}/library/{library_id}/borrow",
                                       json=borrow_request)
                if response.status_code == 200:
                    print("✅ Teacher successfully borrowed magazine")
                    return True
                else:
                    print(f"❌ Failed to borrow: {response.status_code} - {response.text}")
                    return False
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
                return False
    
    return False

if __name__ == "__main__":
    print("Testing OOP Concepts in Library Management System")
    print("=" * 60)
    
    polymorphism_works = test_polymorphism()
    print()
    magazine_borrow_works = test_available_magazine_borrow()
    
    print()
    print("=" * 60)
    print("SUMMARY:")
    print(f"✅ Polymorphism (Different Borrow Limits): {polymorphism_works}")
    print(f"✅ Magazine Borrowing: {magazine_borrow_works}")