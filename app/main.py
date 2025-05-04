from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.routes import authors, books, categories, members, loans

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Library Management API",
    description="API for managing library resources - books, authors, members, and loans",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(categories.router)
app.include_router(members.router)
app.include_router(loans.router)


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint returning a welcome message"""
    return {
        "message": "Welcome to the Library Management API",
        "documentation": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify database connection"""
    try:
        # Execute a simple query to test DB connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}