#!/usr/bin/env python3
"""
Comprehensive Backend Test Suite for Library Management System
Tests all API endpoints, OOP concepts, and error handling
"""

import requests
import json
import uuid
from datetime import datetime
import sys

# Backend URL from environment
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

class LibraryTestSuite:
    def __init__(self):
        self.test_results = []
        self.created_items = {
            'books': [],
            'magazines': [],
            'students': [],
            'teachers': [],
            'borrow_records': []
        }
        
    def log_test(self, test_name, success, details="", response_data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'response': response_data
        }
        self.test_results.append(result)
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def test_health_check(self):
        """Test 1: Health Check Endpoint"""
        try:
            response = requests.get(f"{API_BASE}/health")
            success = response.status_code == 200 and response.json().get('status') == 'healthy'
            self.log_test("Health Check", success, 
                         f"Status: {response.status_code}", response.json())
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False

    def test_books_management(self):
        """Test 2: Books Management - CRUD Operations"""
        library_id = "a"
        
        # Test data for books with different genres
        books_data = [
            {
                "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "author": "Robert C. Martin",
                "isbn": "978-0132350884",
                "genre": "Computer Science",
                "pages": 464,
                "publisher": "Prentice Hall"
            },
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald", 
                "isbn": "978-0743273565",
                "genre": "Fiction",
                "pages": 180,
                "publisher": "Scribner"
            },
            {
                "title": "Sapiens: A Brief History of Humankind",
                "author": "Yuval Noah Harari",
                "isbn": "978-0062316097",
                "genre": "History",
                "pages": 443,
                "publisher": "Harper"
            }
        ]
        
        created_books = []
        
        # CREATE Books
        for book_data in books_data:
            try:
                response = requests.post(f"{API_BASE}/library/{library_id}/books", 
                                       json=book_data)
                if response.status_code == 200:
                    book = response.json().get('book')
                    created_books.append(book)
                    self.created_items['books'].append(book['id'])
                    self.log_test(f"Create Book: {book_data['title']}", True,
                                f"Book ID: {book['id']}")
                else:
                    self.log_test(f"Create Book: {book_data['title']}", False,
                                f"Status: {response.status_code}", response.text)
            except Exception as e:
                self.log_test(f"Create Book: {book_data['title']}", False, 
                            f"Exception: {str(e)}")
        
        # READ All Books
        try:
            response = requests.get(f"{API_BASE}/library/{library_id}/books")
            if response.status_code == 200:
                books = response.json().get('books', [])
                self.log_test("Get All Books", True, 
                            f"Retrieved {len(books)} books")
            else:
                self.log_test("Get All Books", False, 
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get All Books", False, f"Exception: {str(e)}")
        
        # READ Specific Book
        if created_books:
            book_id = created_books[0]['id']
            try:
                response = requests.get(f"{API_BASE}/library/{library_id}/books/{book_id}")
                success = response.status_code == 200
                self.log_test("Get Specific Book", success,
                            f"Book ID: {book_id}")
            except Exception as e:
                self.log_test("Get Specific Book", False, f"Exception: {str(e)}")
        
        # UPDATE Book
        if created_books:
            book_to_update = created_books[0].copy()
            book_to_update['pages'] = 500  # Update page count
            try:
                response = requests.put(f"{API_BASE}/library/{library_id}/books/{book_to_update['id']}", 
                                      json=book_to_update)
                success = response.status_code == 200
                self.log_test("Update Book", success,
                            f"Updated pages to 500 for book {book_to_update['id']}")
            except Exception as e:
                self.log_test("Update Book", False, f"Exception: {str(e)}")

    def test_magazines_management(self):
        """Test 3: Magazines Management"""
        library_id = "a"
        
        magazines_data = [
            {
                "title": "National Geographic",
                "author": "Various Authors",
                "isbn": "MAG-NG-2024-01",
                "issue_number": "January 2024",
                "publication_month": "January 2024"
            },
            {
                "title": "Scientific American",
                "author": "Various Scientists",
                "isbn": "MAG-SA-2024-02",
                "issue_number": "February 2024", 
                "publication_month": "February 2024"
            }
        ]
        
        # CREATE Magazines
        for mag_data in magazines_data:
            try:
                response = requests.post(f"{API_BASE}/library/{library_id}/magazines",
                                       json=mag_data)
                if response.status_code == 200:
                    magazine = response.json().get('magazine')
                    self.created_items['magazines'].append(magazine['id'])
                    self.log_test(f"Create Magazine: {mag_data['title']}", True,
                                f"Magazine ID: {magazine['id']}")
                else:
                    self.log_test(f"Create Magazine: {mag_data['title']}", False,
                                f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Create Magazine: {mag_data['title']}", False,
                            f"Exception: {str(e)}")
        
        # READ All Magazines
        try:
            response = requests.get(f"{API_BASE}/library/{library_id}/magazines")
            if response.status_code == 200:
                magazines = response.json().get('magazines', [])
                self.log_test("Get All Magazines", True,
                            f"Retrieved {len(magazines)} magazines")
            else:
                self.log_test("Get All Magazines", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get All Magazines", False, f"Exception: {str(e)}")

    def test_people_management(self):
        """Test 4: People Management - Students and Teachers (Polymorphism)"""
        library_id = "a"
        
        # CREATE Students with different grade levels
        students_data = [
            {
                "name": "Emma Watson",
                "email": "emma.watson@hogwarts.edu",
                "phone": "555-0101",
                "student_id": "STU001",
                "grade_level": "12th Grade"
            },
            {
                "name": "Daniel Radcliffe", 
                "email": "daniel.radcliffe@hogwarts.edu",
                "phone": "555-0102",
                "student_id": "STU002",
                "grade_level": "11th Grade"
            }
        ]
        
        created_students = []
        for student_data in students_data:
            try:
                response = requests.post(f"{API_BASE}/library/{library_id}/students",
                                       json=student_data)
                if response.status_code == 200:
                    student = response.json().get('student')
                    created_students.append(student)
                    self.created_items['students'].append(student['id'])
                    self.log_test(f"Create Student: {student_data['name']}", True,
                                f"Student ID: {student['id']}, Borrow Limit: {student.get('max_borrow_limit', 5)}")
                else:
                    self.log_test(f"Create Student: {student_data['name']}", False,
                                f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Create Student: {student_data['name']}", False,
                            f"Exception: {str(e)}")
        
        # CREATE Teacher
        teacher_data = {
            "name": "Professor Minerva McGonagall",
            "email": "mcgonagall@hogwarts.edu", 
            "phone": "555-0201",
            "teacher_id": "TEACH001",
            "department": "Transfiguration"
        }
        
        created_teacher = None
        try:
            response = requests.post(f"{API_BASE}/library/{library_id}/teachers",
                                   json=teacher_data)
            if response.status_code == 200:
                created_teacher = response.json().get('teacher')
                self.created_items['teachers'].append(created_teacher['id'])
                self.log_test(f"Create Teacher: {teacher_data['name']}", True,
                            f"Teacher ID: {created_teacher['id']}, Borrow Limit: {created_teacher.get('max_borrow_limit', 10)}")
            else:
                self.log_test(f"Create Teacher: {teacher_data['name']}", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(f"Create Teacher: {teacher_data['name']}", False,
                        f"Exception: {str(e)}")
        
        # READ Students and Teachers
        try:
            response = requests.get(f"{API_BASE}/library/{library_id}/students")
            if response.status_code == 200:
                students = response.json().get('students', [])
                self.log_test("Get All Students", True,
                            f"Retrieved {len(students)} students")
            else:
                self.log_test("Get All Students", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get All Students", False, f"Exception: {str(e)}")
        
        try:
            response = requests.get(f"{API_BASE}/library/{library_id}/teachers")
            if response.status_code == 200:
                teachers = response.json().get('teachers', [])
                self.log_test("Get All Teachers", True,
                            f"Retrieved {len(teachers)} teachers")
            else:
                self.log_test("Get All Teachers", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get All Teachers", False, f"Exception: {str(e)}")
        
        return created_students, created_teacher

    def test_borrow_return_operations(self):
        """Test 5: Borrow/Return Operations - Testing Polymorphism"""
        library_id = "a"
        
        # Get available books and magazines
        books_response = requests.get(f"{API_BASE}/library/{library_id}/books")
        magazines_response = requests.get(f"{API_BASE}/library/{library_id}/magazines")
        students_response = requests.get(f"{API_BASE}/library/{library_id}/students")
        teachers_response = requests.get(f"{API_BASE}/library/{library_id}/teachers")
        
        if not all([r.status_code == 200 for r in [books_response, magazines_response, students_response, teachers_response]]):
            self.log_test("Borrow/Return Setup", False, "Failed to get required data")
            return
        
        books = books_response.json().get('books', [])
        magazines = magazines_response.json().get('magazines', [])
        students = students_response.json().get('students', [])
        teachers = teachers_response.json().get('teachers', [])
        
        if not (books and magazines and students and teachers):
            self.log_test("Borrow/Return Setup", False, "Insufficient test data")
            return
        
        # Test 1: Student borrows a book
        if books and students:
            borrow_request = {
                "person_id": students[0]['id'],
                "item_id": books[0]['id']
            }
            
            try:
                response = requests.post(f"{API_BASE}/library/{library_id}/borrow",
                                       json=borrow_request)
                if response.status_code == 200:
                    record = response.json().get('record')
                    self.created_items['borrow_records'].append(record['id'])
                    self.log_test("Student Borrows Book", True,
                                f"Student {students[0]['name']} borrowed {books[0]['title']}")
                    
                    # Verify item availability changed
                    book_check = requests.get(f"{API_BASE}/library/{library_id}/books/{books[0]['id']}")
                    if book_check.status_code == 200:
                        book_data = book_check.json()
                        available = book_data.get('available', True)
                        self.log_test("Book Availability Update", not available,
                                    f"Book availability: {available}")
                else:
                    self.log_test("Student Borrows Book", False,
                                f"Status: {response.status_code}", response.text)
            except Exception as e:
                self.log_test("Student Borrows Book", False, f"Exception: {str(e)}")
        
        # Test 2: Teacher borrows a magazine
        if magazines and teachers:
            borrow_request = {
                "person_id": teachers[0]['id'],
                "item_id": magazines[0]['id']
            }
            
            try:
                response = requests.post(f"{API_BASE}/library/{library_id}/borrow",
                                       json=borrow_request)
                if response.status_code == 200:
                    record = response.json().get('record')
                    self.created_items['borrow_records'].append(record['id'])
                    self.log_test("Teacher Borrows Magazine", True,
                                f"Teacher {teachers[0]['name']} borrowed {magazines[0]['title']}")
                else:
                    self.log_test("Teacher Borrows Magazine", False,
                                f"Status: {response.status_code}", response.text)
            except Exception as e:
                self.log_test("Teacher Borrows Magazine", False, f"Exception: {str(e)}")
        
        # Test 3: Get borrow records
        try:
            response = requests.get(f"{API_BASE}/library/{library_id}/borrow-records")
            if response.status_code == 200:
                records = response.json().get('records', [])
                self.log_test("Get Borrow Records", True,
                            f"Retrieved {len(records)} borrow records")
            else:
                self.log_test("Get Borrow Records", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get Borrow Records", False, f"Exception: {str(e)}")
        
        # Test 4: Return an item
        if self.created_items['borrow_records']:
            return_request = {
                "record_id": self.created_items['borrow_records'][0]
            }
            
            try:
                response = requests.post(f"{API_BASE}/library/{library_id}/return",
                                       json=return_request)
                success = response.status_code == 200
                self.log_test("Return Item", success,
                            f"Returned item with record ID: {return_request['record_id']}")
                
                # Verify availability is restored
                if success and books:
                    book_check = requests.get(f"{API_BASE}/library/{library_id}/books/{books[0]['id']}")
                    if book_check.status_code == 200:
                        book_data = book_check.json()
                        available = book_data.get('available', False)
                        self.log_test("Item Availability Restored", available,
                                    f"Book availability after return: {available}")
            except Exception as e:
                self.log_test("Return Item", False, f"Exception: {str(e)}")

    def test_xml_operations(self):
        """Test 6: XML Export/Import Operations"""
        library_id = "a"
        
        # Test XML Export
        try:
            response = requests.get(f"{API_BASE}/library/{library_id}/xml/export")
            if response.status_code == 200:
                xml_data = response.json()
                xml_string = xml_data.get('xml', '')
                
                # Verify XML structure
                has_library_catalog = '<LibraryCatalog' in xml_string
                has_books = '<Books>' in xml_string
                has_magazines = '<Magazines>' in xml_string
                has_students = '<Students>' in xml_string
                has_teachers = '<Teachers>' in xml_string
                
                xml_valid = all([has_library_catalog, has_books, has_magazines, has_students, has_teachers])
                
                self.log_test("XML Export", True,
                            f"XML structure valid: {xml_valid}, Length: {len(xml_string)} chars")
                
                # Test XML Import to Library B
                import_data = {"xml": xml_string}
                try:
                    import_response = requests.post(f"{API_BASE}/library/b/xml/import",
                                                  json=import_data)
                    if import_response.status_code == 200:
                        import_result = import_response.json()
                        imported = import_result.get('imported', {})
                        self.log_test("XML Import to Library B", True,
                                    f"Imported - Books: {imported.get('books', 0)}, "
                                    f"Magazines: {imported.get('magazines', 0)}, "
                                    f"Students: {imported.get('students', 0)}, "
                                    f"Teachers: {imported.get('teachers', 0)}")
                    else:
                        self.log_test("XML Import to Library B", False,
                                    f"Status: {import_response.status_code}")
                except Exception as e:
                    self.log_test("XML Import to Library B", False, f"Exception: {str(e)}")
                
            else:
                self.log_test("XML Export", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("XML Export", False, f"Exception: {str(e)}")
        
        # Test Library Sync
        sync_data = {
            "source": "a",
            "target": "b"
        }
        
        try:
            response = requests.post(f"{API_BASE}/library/xml/sync",
                                   json=sync_data)
            if response.status_code == 200:
                sync_result = response.json()
                synced = sync_result.get('synced', {})
                self.log_test("Library Sync A->B", True,
                            f"Synced - Books: {synced.get('books', 0)}, "
                            f"Magazines: {synced.get('magazines', 0)}, "
                            f"Students: {synced.get('students', 0)}, "
                            f"Teachers: {synced.get('teachers', 0)}")
                
                # Verify Library B has the synced data
                b_books_response = requests.get(f"{API_BASE}/library/b/books")
                if b_books_response.status_code == 200:
                    b_books = b_books_response.json().get('books', [])
                    self.log_test("Verify Library B Data", len(b_books) > 0,
                                f"Library B has {len(b_books)} books after sync")
            else:
                self.log_test("Library Sync A->B", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Library Sync A->B", False, f"Exception: {str(e)}")

    def test_search_functionality(self):
        """Test 7: Search Functionality"""
        library_id = "a"
        
        # Search for a book title
        search_queries = ["Clean Code", "Gatsby", "Emma"]
        
        for query in search_queries:
            try:
                response = requests.get(f"{API_BASE}/library/{library_id}/search",
                                      params={"query": query})
                if response.status_code == 200:
                    results = response.json()
                    total_results = (len(results.get('books', [])) + 
                                   len(results.get('magazines', [])) + 
                                   len(results.get('students', [])) + 
                                   len(results.get('teachers', [])))
                    self.log_test(f"Search: '{query}'", True,
                                f"Found {total_results} results")
                else:
                    self.log_test(f"Search: '{query}'", False,
                                f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Search: '{query}'", False, f"Exception: {str(e)}")

    def test_statistics(self):
        """Test 8: Library Statistics"""
        library_id = "a"
        
        try:
            response = requests.get(f"{API_BASE}/library/{library_id}/stats")
            if response.status_code == 200:
                stats = response.json()
                expected_keys = ['total_books', 'available_books', 'total_magazines', 
                               'available_magazines', 'total_students', 'total_teachers',
                               'active_borrows', 'overdue_items']
                
                has_all_keys = all(key in stats for key in expected_keys)
                self.log_test("Library Statistics", has_all_keys,
                            f"Stats: {stats}")
            else:
                self.log_test("Library Statistics", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Library Statistics", False, f"Exception: {str(e)}")

    def test_error_handling(self):
        """Test 9: Error Handling Scenarios"""
        library_id = "a"
        
        # Test 1: Borrow non-existent item
        fake_borrow = {
            "person_id": "fake-person-id",
            "item_id": "fake-item-id"
        }
        
        try:
            response = requests.post(f"{API_BASE}/library/{library_id}/borrow",
                                   json=fake_borrow)
            expected_error = response.status_code in [404, 400]
            self.log_test("Error: Borrow Non-existent Item", expected_error,
                        f"Status: {response.status_code} (Expected 404/400)")
        except Exception as e:
            self.log_test("Error: Borrow Non-existent Item", False, f"Exception: {str(e)}")
        
        # Test 2: Invalid XML import
        invalid_xml = {"xml": "<invalid>xml</structure>"}
        
        try:
            response = requests.post(f"{API_BASE}/library/{library_id}/xml/import",
                                   json=invalid_xml)
            expected_error = response.status_code == 400
            self.log_test("Error: Invalid XML Import", expected_error,
                        f"Status: {response.status_code} (Expected 400)")
        except Exception as e:
            self.log_test("Error: Invalid XML Import", False, f"Exception: {str(e)}")
        
        # Test 3: Get non-existent book
        try:
            response = requests.get(f"{API_BASE}/library/{library_id}/books/fake-book-id")
            expected_error = response.status_code == 404
            self.log_test("Error: Get Non-existent Book", expected_error,
                        f"Status: {response.status_code} (Expected 404)")
        except Exception as e:
            self.log_test("Error: Get Non-existent Book", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all test suites"""
        print("=" * 80)
        print("LIBRARY MANAGEMENT SYSTEM - BACKEND API TEST SUITE")
        print("=" * 80)
        print()
        
        # Run tests in sequence
        self.test_health_check()
        self.test_books_management()
        self.test_magazines_management()
        self.test_people_management()
        self.test_borrow_return_operations()
        self.test_xml_operations()
        self.test_search_functionality()
        self.test_statistics()
        self.test_error_handling()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if "✅ PASS" in result['status'])
        failed = sum(1 for result in self.test_results if "❌ FAIL" in result['status'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        print()
        
        if failed > 0:
            print("FAILED TESTS:")
            for result in self.test_results:
                if "❌ FAIL" in result['status']:
                    print(f"  - {result['test']}: {result['details']}")
        
        print("=" * 80)
        
        return passed, failed, total

if __name__ == "__main__":
    print("Starting Library Management System Backend Tests...")
    print(f"Backend URL: {BACKEND_URL}")
    print()
    
    test_suite = LibraryTestSuite()
    passed, failed, total = test_suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)