from fastapi import APIRouter
from mongo_ops import library_db
from utils.customHandlers import customResponse, customObjectId
import datetime
from models import Book
from bson import ObjectId

"""
Below are 5 books data related endpoints:
1. /books           - GET    - Returns all the books data present in the Books DB.
2. /books           - POST   - Adds data for one more book in the Books DB.
3. /books/{book_id} - GET    - Returns data for the book matching with the given id.
4. /books/{book_id} - PUT    - Updates data for the book matching with the given id.
5. /books/{book_id} - DELETE - Removes data for the book matching with the given id.
"""
router = APIRouter()
books_collection = library_db.books

# Get all the books in the DB
@router.get("/books")
async def get_all_books():
    res = await books_collection.find().to_list(None)
    return customResponse(res)

# Get a specific book from the DB
@router.get("/books/{book_id}")
async def get_book(book_id: customObjectId):
    res = await books_collection.find_one({'_id': book_id})
    return customResponse(res)

# Add another book in the DB
@router.post("/books")
async def add_book(book: Book):
    res = await books_collection.insert_one({
        'name': book.name,
        'author': book.author,
        'num_issued': book.num_issued,
        'date_added': datetime.datetime.now(),
        'date_updated': datetime.datetime.now() 
    })

    if res.acknowledged:
        return {'insert_id': str(res.inserted_id)}
    return {'status': 'unable to add data'}

# Update a books data in the DB
@router.put("/books/{book_id}")
async def update_book_data(book_id: customObjectId, book: Book):
    updated_data = {'date_updated': datetime.datetime.now()}
    if book.name:
        updated_data.update({'name': book.name})
    if book.author:
        updated_data.update({'author': book.author})
    if book.num_issued:
        updated_data.update({'num_issued': book.num_issued})
    res = await books_collection.update_one({'_id': book_id}, {"$set": updated_data})

    if res.acknowledged:
        return {'status': f'found {res.matched_count} entries, and updated {res.modified_count} entries'}
    return {'status': 'unable to delete data'}

# Delete a books data from the DB
@router.delete("/books/{book_id}")
async def delete_book_data(book_id: customObjectId):
    res = await books_collection.delete_one({'_id': book_id})
    if res.acknowledged:
        return {'status': f'deleted {res.deleted_count} entries'}
    return {'status': 'unable to delete data'}
