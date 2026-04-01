from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import db 
from pydantic import BaseModel
from bson import ObjectId
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

class Book(BaseModel):
    title: str
    author: str
    pages: str
@app.post("/add-book")
async def add_book(book: Book):
    # .model_dump() is the Pydantic v2 way to get a dict
    result = await db.books.insert_one(book.model_dump())
    return {"id": str(result.inserted_id), "status": "Book Saved Successfully"}

@app.get("/list-books")
async def list_books():
    books = await db.books.find().to_list(100)
    for b in books: 
        b["_id"] = str(b["_id"]) 
    return books

@app.delete("/delete-book/{book_id}")
async def delete_book(book_id: str):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db.books.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 1:
        return {"status": "Success"}
    return {"status": "Error", "message": "Book not found"}