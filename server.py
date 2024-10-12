from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
import sqlite3

app = FastAPI()

# Pydantic model to create a base model for what a Book should look like.
class Book(BaseModel):
    title: str
    author: str
    published_date: str

def create_database():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            published_date TEXT
            )
         ''')

    connection.commit()
    connection.close()

@app.get("/books")
def list_books():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    connection.close()
    return [{'id': book[0], 'title': book[1], 'author': book[2], 'published_date': book[3]}
        for book in books]

@app.get("/books/{book_id}")
def get_specific_book(book_id: int):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    connection.close()
    if book:
        return {'id': book[0], 'title': book[1], 'author': book[2], 'published_date': book[3]}
    return {"error": "Book not found"}


@app.post("/books")
def add_books(book: Book):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute("""
                 INSERT INTO books (title, author, published_date)
                 VALUES (?, ?, ?)""", (book.title, book.author, book.published_date)
            )
    connection.commit()
    connection.close()
    return {'message': 'Book added successfully'}



@app.put("/books/{book_id}")
def update_book(book_id : int, book: Book):
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    cursor.execute("""
            UPDATE books
            SET title = ?, author = ?, published_date = ?
                   WHERE id = ?""",
                   (book.title, book.author, book.published_date, book_id))
    connection.commit()
    connection.close()
    return {'message': 'Book updated successfully'}


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)
    create_database()
