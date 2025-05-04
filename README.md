# Library Management System API

A FastAPI application for managing library resources including books, authors, members, and loans.

## Features

- **Books Management**: Add, update, delete, and list books
- **Authors Management**: Track author information and their works
- **Member Management**: Manage library members and their statuses
- **Loan Management**: Track book loans, returns, and calculate fines
- **Categories Management**: Organize books by categories

## Database Schema

The system uses MySQL with the following tables:
- **authors**: Information about book authors
- **books**: Details about books in the library
- **book_authors**: Many-to-many relationship between books and authors
- **categories**: Book categories/genres
- **members**: Library member information
- **loans**: Records of book loans and returns

## API Endpoints

### Books
- `GET /books` - List all books (with filtering options)
- `GET /books/{book_id}` - Get a specific book
- `POST /books` - Add a new book
- `PUT /books/{book_id}` - Update book information
- `DELETE /books/{book_id}` - Remove a book

### Authors
- `GET /authors` - List all authors
- `GET /authors/{author_id}` - Get a specific author
- `POST /authors` - Add a new author
- `PUT /authors/{author_id}` - Update author information
- `DELETE /authors/{author_id}` - Remove an author

### Categories
- `GET /categories` - List all categories
- `GET /categories/{category_id}` - Get a specific category
- `POST /categories` - Add a new category
- `PUT /categories/{category_id}` - Update category information
- `DELETE /categories/{category_id}` - Remove a category

### Members
- `GET /members` - List all members (with filtering options)
- `GET /members/{member_id}` - Get a specific member
- `POST /members` - Add a new member
- `PUT /members/{member_id}` - Update member information
- `DELETE /members/{member_id}` - Remove a member

### Loans
- `GET /loans` - List all loans (with filtering options)
- `GET /loans/{loan_id}` - Get a specific loan
- `POST /loans` - Create a new loan
- `PUT /loans/{loan_id}` - Update loan information
- `DELETE /loans/{loan_id}` - Remove a loan
- `POST /loans/{loan_id}/return` - Return a book

## Setup and Installation

1. Clone the repository
2. Create a MySQL database named `library_management`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Update database connection settings in `app/database.py`
5. Run the application:
   ```
   uvicorn app.main:app --reload
   ```
6. Access the API documentation at `http://localhost:8000/docs`

## Technologies Used

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **MySQL**: Relational database

## License

