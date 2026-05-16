# Structuring a FastAPI Project: Best Practices

FastAPI is a powerful and efficient web framework for building APIs with Python. However, as projects grow, organizing the code properly becomes crucial for maintainability and scalability. This article outlines a structured approach to organizing FastAPI projects, inspired by the official documentation and best practices.

## Recommended FastAPI Project Structure

A well-structured FastAPI project should separate concerns into different modules, ensuring clear boundaries between routing, models, schemas, services, and database interactions. Below is a directory structure that works well for most projects:

```
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── internal/
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── db/
│       ├── __init__.py
│       ├── database.py
│       └── migrations/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_users.py
│   ├── test_items.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── run.sh
```

## Explanation of the Structure with Examples

### 1. Main Application (app/)

- main.py: The entry point of the FastAPI application.

```python
from fastapi import FastAPI
from app.routers import users, items

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
```

- dependencies.py: Contains shared dependencies like database sessions.

```python
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()
```

### 2. Routers (app/routers/)

Handles API endpoints:

- users.py:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.services.user_service import create_user
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserCreate)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
return create_user(db, user)
```

### 3. Internal (app/internal/)

Contains internal, non-public endpoints, such as an admin panel.

- admin.py:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def get_admin_dashboard():
return {"message": "Admin Dashboard"}
```

### 4. Core (app/core/)

Holds configurations and security settings:

- config.py:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
security.py:
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
return pwd_context.hash(password)
```

### 5. Models (app/models/)

Defines SQLAlchemy models:

- user.py:

```python
from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
**tablename** = "users"
id = Column(Integer, primary_key=True, index=True)
username = Column(String, unique=True, index=True)
password_hash = Column(String)
```

### 6. Schemas (app/schemas/)

Pydantic models for data validation:

- user.py:

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
username: str
password: str
```

### 7. Services (app/services/)

Contains business logic separate from API routes:

- user_service.py:

```python
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def create_user(db: Session, user: UserCreate):
db_user = User(username=user.username, password_hash=hash_password(user.password))
db.add(db_user)
db.commit()
db.refresh(db_user)
return db_user
```

### 8. Database (app/db/)

- database.py:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### 9. Tests (tests/)

Includes unit and integration tests:

- test_users.py:

```python
def test_create_user():
response = client.post("/users/", json={"username": "testuser", "password": "testpass"})
assert response.status_code == 200
assert response.json()["username"] == "testuser"
```

Conclusion
By structuring your FastAPI project properly, you ensure better scalability, maintainability, and testability. Following this structure allows developers to collaborate efficiently and keep the code clean and organized.

💬What is your opinion?
Do you think a different structure would work better?
