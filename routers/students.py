import datetime
from fastapi import APIRouter
from mongo_ops import library_db
from models import Student
from utils.customHandlers import customResponse

"""
Below are 5 student data related endpoints:
1. /students              - GET    - Returns all the students data present in the Students DB.
2. /students              - POST   - Adds data for one more student in the Students DB.
3. /students/{student_id} - GET    - Returns data for the student matching with the given id.
4. /students/{student_id} - PUT    - Updates data for the student matching with the given id.
5. /students/{student_id} - DELETE - Removes data for the student matching with the given id.
"""
 
router = APIRouter()
students_collection = library_db.students

# Get all the students in the DB
@router.get("/students")
async def get_all_students():
    res = await students_collection.find().to_list(None)
    return customResponse(res)

# Get a specific student from the DB
@router.get("/students/{student_id}")
async def get_student(student_id: int):
    res = await students_collection.find_one({'id': student_id})
    return customResponse(res)

# Add another student in the DB
@router.post("/students")
async def add_student(student: Student):
    res = await students_collection.insert_one({
        'name': student.name,
        'id': student.id,
        'school':student.school, 
        'date_added': datetime.datetime.now(),
        'date_updated': datetime.datetime.now() 
    })

    if res.acknowledged:
        return {'insert_id': str(res.inserted_id)}
    return {'status': 'unable to add data'}

# Update a students data in the DB
@router.put("/students/{student_id}")
async def update_student_data(student_id: int, student: Student):
    updated_data = {'date_updated': datetime.datetime.now()}
    if student.name:
        updated_data.update({'name': student.name})
    if student.id:
        updated_data.update({'id': student.id})
    if student.school:
        updated_data.update({'school': student.school})
    if student.num_books_issued:
        updated_data.update({'num_books_issued': student.num_books_issued})
    if student.has_currently_issued_book:
        updated_data.update({'has_currently_issued_book': student.has_currently_issued_book})
    res = await students_collection.update_one({'id': student_id}, {"$set": updated_data})
    print(res)
    if res.acknowledged:
        return {'status': f'found {res.matched_count} entries, and updated {res.modified_count} entries'}
    return {'status': 'unable to delete data'}
    

# Delete a students data from the DB
@router.delete("/students/{student_id}")
async def delete_student_data(student_id: int):
    res = await students_collection.delete_one({'id': student_id})
    if res.acknowledged:
        return {'status': f'deleted {res.deleted_count} entries'}
    return {'status': 'unable to delete data'}
