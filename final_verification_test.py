#!/usr/bin/env python3
"""
Final Verification Test - Key Library Management System Features
"""

import requests
import json

BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

def test_key_endpoints():
    """Test all key endpoints with minimal data"""
    results = []
    
    # 1. Health Check
    try:
        response = requests.get(f"{API_BASE}/health")
        results.append(("Health Check", response.status_code == 200))
    except:
        results.append(("Health Check", False))
    
    # 2. Get Library A Stats
    try:
        response = requests.get(f"{API_BASE}/library/a/stats")
        if response.status_code == 200:
            stats = response.json()
            has_required_keys = all(key in stats for key in ['total_books', 'total_students', 'total_teachers'])
            results.append(("Library Statistics", has_required_keys))
        else:
            results.append(("Library Statistics", False))
    except:
        results.append(("Library Statistics", False))
    
    # 3. Get Books
    try:
        response = requests.get(f"{API_BASE}/library/a/books")
        results.append(("Get Books", response.status_code == 200))
    except:
        results.append(("Get Books", False))
    
    # 4. Get Magazines
    try:
        response = requests.get(f"{API_BASE}/library/a/magazines")
        results.append(("Get Magazines", response.status_code == 200))
    except:
        results.append(("Get Magazines", False))
    
    # 5. Get Students
    try:
        response = requests.get(f"{API_BASE}/library/a/students")
        results.append(("Get Students", response.status_code == 200))
    except:
        results.append(("Get Students", False))
    
    # 6. Get Teachers
    try:
        response = requests.get(f"{API_BASE}/library/a/teachers")
        results.append(("Get Teachers", response.status_code == 200))
    except:
        results.append(("Get Teachers", False))
    
    # 7. Get Borrow Records
    try:
        response = requests.get(f"{API_BASE}/library/a/borrow-records")
        results.append(("Get Borrow Records", response.status_code == 200))
    except:
        results.append(("Get Borrow Records", False))
    
    # 8. Search Functionality
    try:
        response = requests.get(f"{API_BASE}/library/a/search", params={"query": "Code"})
        results.append(("Search Functionality", response.status_code == 200))
    except:
        results.append(("Search Functionality", False))
    
    # 9. XML Export
    try:
        response = requests.get(f"{API_BASE}/library/a/xml/export")
        if response.status_code == 200:
            xml_data = response.json().get('xml', '')
            xml_valid = '<LibraryCatalog' in xml_data and '</LibraryCatalog>' in xml_data
            results.append(("XML Export", xml_valid))
        else:
            results.append(("XML Export", False))
    except:
        results.append(("XML Export", False))
    
    # 10. Library Sync
    try:
        sync_data = {"source": "a", "target": "b"}
        response = requests.post(f"{API_BASE}/library/xml/sync", json=sync_data)
        results.append(("Library Sync", response.status_code == 200))
    except:
        results.append(("Library Sync", False))
    
    return results

def verify_oop_concepts():
    """Verify OOP concepts are implemented"""
    results = []
    
    # Check polymorphism in borrow limits
    try:
        students_response = requests.get(f"{API_BASE}/library/a/students")
        teachers_response = requests.get(f"{API_BASE}/library/a/teachers")
        
        if students_response.status_code == 200 and teachers_response.status_code == 200:
            students = students_response.json().get('students', [])
            teachers = teachers_response.json().get('teachers', [])
            
            if students and teachers:
                student_limit = students[0].get('max_borrow_limit', 5)
                teacher_limit = teachers[0].get('max_borrow_limit', 10)
                polymorphism_works = student_limit != teacher_limit
                results.append(("Polymorphism (Borrow Limits)", polymorphism_works))
            else:
                results.append(("Polymorphism (Borrow Limits)", False))
        else:
            results.append(("Polymorphism (Borrow Limits)", False))
    except:
        results.append(("Polymorphism (Borrow Limits)", False))
    
    # Check inheritance in item types
    try:
        books_response = requests.get(f"{API_BASE}/library/a/books")
        magazines_response = requests.get(f"{API_BASE}/library/a/magazines")
        
        if books_response.status_code == 200 and magazines_response.status_code == 200:
            books = books_response.json().get('books', [])
            magazines = magazines_response.json().get('magazines', [])
            
            # Check that books have genre field and magazines have issue_number
            book_inheritance = any('genre' in book for book in books)
            magazine_inheritance = any('issue_number' in mag for mag in magazines)
            
            results.append(("Inheritance (Book/Magazine)", book_inheritance and magazine_inheritance))
        else:
            results.append(("Inheritance (Book/Magazine)", False))
    except:
        results.append(("Inheritance (Book/Magazine)", False))
    
    return results

def main():
    print("=" * 80)
    print("FINAL VERIFICATION TEST - LIBRARY MANAGEMENT SYSTEM")
    print("=" * 80)
    print()
    
    # Test key endpoints
    print("🔍 TESTING KEY API ENDPOINTS:")
    print("-" * 40)
    endpoint_results = test_key_endpoints()
    
    for test_name, success in endpoint_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    
    # Test OOP concepts
    print("🏗️  TESTING OOP CONCEPTS:")
    print("-" * 40)
    oop_results = verify_oop_concepts()
    
    for test_name, success in oop_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    
    # Summary
    all_results = endpoint_results + oop_results
    total_tests = len(all_results)
    passed_tests = sum(1 for _, success in all_results if success)
    failed_tests = total_tests - passed_tests
    
    print("=" * 80)
    print("📊 FINAL SUMMARY:")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    if failed_tests > 0:
        print()
        print("❌ FAILED TESTS:")
        for test_name, success in all_results:
            if not success:
                print(f"  - {test_name}")
    else:
        print()
        print("🎉 ALL TESTS PASSED! Library Management System is working correctly.")
    
    print("=" * 80)

if __name__ == "__main__":
    main()