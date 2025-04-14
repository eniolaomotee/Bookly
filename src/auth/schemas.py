from pydantic import BaseModel, Field
import uuid
from src.books.schemas import Book
from typing import List
from datetime import datetime
from src.reviews.schemas import ReviewModel

class UserCreate(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    username: str = Field(max_length=50)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    
class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash:str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    
class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]
        
class UserLoginModel(BaseModel):
    email:str
    password:str
    
class EmailModel(BaseModel):
    addresses: List[str]
    
class PasswordResetRequestModel(BaseModel):
    email:str
    
class PasswordResetConfirm(BaseModel):
    new_password:str
    confirm_new_password:str