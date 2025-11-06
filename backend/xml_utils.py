import xml.etree.ElementTree as ET
from typing import List, Dict
from datetime import datetime

def export_to_xml(library_id: str, data: Dict) -> str:
    """Export library data to XML format"""
    root = ET.Element('LibraryCatalog')
    root.set('library', f'Library_{library_id.upper()}')
    root.set('export_date', datetime.now().isoformat())
    
    # Export Books
    books_elem = ET.SubElement(root, 'Books')
    for book in data.get('books', []):
        book_elem = ET.SubElement(books_elem, 'Book')
        book_elem.set('type', book.get('genre', 'General'))
        
        ET.SubElement(book_elem, 'ID').text = book['id']
        ET.SubElement(book_elem, 'Title').text = book['title']
        ET.SubElement(book_elem, 'Author').text = book['author']
        ET.SubElement(book_elem, 'ISBN').text = book['isbn']
        ET.SubElement(book_elem, 'Available').text = str(book['available']).lower()
        ET.SubElement(book_elem, 'Pages').text = str(book.get('pages', 0))
        ET.SubElement(book_elem, 'Publisher').text = book.get('publisher', '')
    
    # Export Magazines
    magazines_elem = ET.SubElement(root, 'Magazines')
    for magazine in data.get('magazines', []):
        mag_elem = ET.SubElement(magazines_elem, 'Magazine')
        
        ET.SubElement(mag_elem, 'ID').text = magazine['id']
        ET.SubElement(mag_elem, 'Title').text = magazine['title']
        ET.SubElement(mag_elem, 'Author').text = magazine['author']
        ET.SubElement(mag_elem, 'ISBN').text = magazine['isbn']
        ET.SubElement(mag_elem, 'Available').text = str(magazine['available']).lower()
        ET.SubElement(mag_elem, 'IssueNumber').text = magazine.get('issue_number', '')
        ET.SubElement(mag_elem, 'PublicationMonth').text = magazine.get('publication_month', '')
    
    # Export Students
    students_elem = ET.SubElement(root, 'Students')
    for student in data.get('students', []):
        student_elem = ET.SubElement(students_elem, 'Student')
        
        ET.SubElement(student_elem, 'ID').text = student['id']
        ET.SubElement(student_elem, 'Name').text = student['name']
        ET.SubElement(student_elem, 'Email').text = student['email']
        ET.SubElement(student_elem, 'Phone').text = student['phone']
        ET.SubElement(student_elem, 'StudentID').text = student['student_id']
        ET.SubElement(student_elem, 'GradeLevel').text = student['grade_level']
        ET.SubElement(student_elem, 'MaxBorrowLimit').text = str(student.get('max_borrow_limit', 5))
    
    # Export Teachers
    teachers_elem = ET.SubElement(root, 'Teachers')
    for teacher in data.get('teachers', []):
        teacher_elem = ET.SubElement(teachers_elem, 'Teacher')
        
        ET.SubElement(teacher_elem, 'ID').text = teacher['id']
        ET.SubElement(teacher_elem, 'Name').text = teacher['name']
        ET.SubElement(teacher_elem, 'Email').text = teacher['email']
        ET.SubElement(teacher_elem, 'Phone').text = teacher['phone']
        ET.SubElement(teacher_elem, 'TeacherID').text = teacher['teacher_id']
        ET.SubElement(teacher_elem, 'Department').text = teacher['department']
        ET.SubElement(teacher_elem, 'MaxBorrowLimit').text = str(teacher.get('max_borrow_limit', 10))
    
    # Convert to string with pretty formatting
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding='unicode', method='xml')

def import_from_xml(xml_string: str) -> Dict:
    """Import library data from XML format"""
    root = ET.fromstring(xml_string)
    
    data = {
        'books': [],
        'magazines': [],
        'students': [],
        'teachers': []
    }
    
    # Import Books
    books_elem = root.find('Books')
    if books_elem is not None:
        for book_elem in books_elem.findall('Book'):
            book = {
                'id': book_elem.find('ID').text if book_elem.find('ID') is not None else '',
                'title': book_elem.find('Title').text if book_elem.find('Title') is not None else '',
                'author': book_elem.find('Author').text if book_elem.find('Author') is not None else '',
                'isbn': book_elem.find('ISBN').text if book_elem.find('ISBN') is not None else '',
                'available': book_elem.find('Available').text == 'true' if book_elem.find('Available') is not None else True,
                'genre': book_elem.get('type', 'General'),
                'pages': int(book_elem.find('Pages').text) if book_elem.find('Pages') is not None and book_elem.find('Pages').text else 0,
                'publisher': book_elem.find('Publisher').text if book_elem.find('Publisher') is not None else '',
                'item_type': 'book'
            }
            data['books'].append(book)
    
    # Import Magazines
    magazines_elem = root.find('Magazines')
    if magazines_elem is not None:
        for mag_elem in magazines_elem.findall('Magazine'):
            magazine = {
                'id': mag_elem.find('ID').text if mag_elem.find('ID') is not None else '',
                'title': mag_elem.find('Title').text if mag_elem.find('Title') is not None else '',
                'author': mag_elem.find('Author').text if mag_elem.find('Author') is not None else '',
                'isbn': mag_elem.find('ISBN').text if mag_elem.find('ISBN') is not None else '',
                'available': mag_elem.find('Available').text == 'true' if mag_elem.find('Available') is not None else True,
                'issue_number': mag_elem.find('IssueNumber').text if mag_elem.find('IssueNumber') is not None else '',
                'publication_month': mag_elem.find('PublicationMonth').text if mag_elem.find('PublicationMonth') is not None else '',
                'item_type': 'magazine'
            }
            data['magazines'].append(magazine)
    
    # Import Students
    students_elem = root.find('Students')
    if students_elem is not None:
        for student_elem in students_elem.findall('Student'):
            student = {
                'id': student_elem.find('ID').text if student_elem.find('ID') is not None else '',
                'name': student_elem.find('Name').text if student_elem.find('Name') is not None else '',
                'email': student_elem.find('Email').text if student_elem.find('Email') is not None else '',
                'phone': student_elem.find('Phone').text if student_elem.find('Phone') is not None else '',
                'student_id': student_elem.find('StudentID').text if student_elem.find('StudentID') is not None else '',
                'grade_level': student_elem.find('GradeLevel').text if student_elem.find('GradeLevel') is not None else '',
                'max_borrow_limit': int(student_elem.find('MaxBorrowLimit').text) if student_elem.find('MaxBorrowLimit') is not None and student_elem.find('MaxBorrowLimit').text else 5,
                'person_type': 'student'
            }
            data['students'].append(student)
    
    # Import Teachers
    teachers_elem = root.find('Teachers')
    if teachers_elem is not None:
        for teacher_elem in teachers_elem.findall('Teacher'):
            teacher = {
                'id': teacher_elem.find('ID').text if teacher_elem.find('ID') is not None else '',
                'name': teacher_elem.find('Name').text if teacher_elem.find('Name') is not None else '',
                'email': teacher_elem.find('Email').text if teacher_elem.find('Email') is not None else '',
                'phone': teacher_elem.find('Phone').text if teacher_elem.find('Phone') is not None else '',
                'teacher_id': teacher_elem.find('TeacherID').text if teacher_elem.find('TeacherID') is not None else '',
                'department': teacher_elem.find('Department').text if teacher_elem.find('Department') is not None else '',
                'max_borrow_limit': int(teacher_elem.find('MaxBorrowLimit').text) if teacher_elem.find('MaxBorrowLimit') is not None and teacher_elem.find('MaxBorrowLimit').text else 10,
                'person_type': 'teacher'
            }
            data['teachers'].append(teacher)
    
    return data

def validate_xml(xml_string: str) -> bool:
    """Validate XML format"""
    try:
        root = ET.fromstring(xml_string)
        return root.tag == 'LibraryCatalog'
    except ET.ParseError:
        return False