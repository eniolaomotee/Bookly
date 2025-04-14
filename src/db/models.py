from sqlmodel import Field, SQLModel,Field,Column,Relationship
import sqlalchemy.dialects.postgresql as pg
from typing import List
import uuid
from datetime import datetime
from typing import Optional,List


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        ))
    username: str
    email:str
    first_name: str
    last_name: str
    role : str  = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified:bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    # Relationship with the Book model
    books : List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy':'selectin'} )
    # Relationship with the Review model
    reviews : List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy':'selectin'} )

    
    
    
    
    # Method that gives a string representation of the user object in our db
    def __repr__(self):
        return f"<User {self.username}>"

class BookTag(SQLModel, table=True): 
    book_uid: uuid.UUID = Field(foreign_key="books.uid", primary_key=True)
    tag_uid: uuid.UUID = Field(foreign_key="tags.uid", primary_key=True)


class Book(SQLModel, table=True):
    __tablename__ = "books"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        ))
    title:str
    author:str
    publisher:str
    published_date: datetime
    page_count:int
    language:str
    user_uid: Optional[uuid.UUID] = Field(default= None, foreign_key="users.uid")
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    # Relationship with the user model
    user : Optional["User"] = Relationship(back_populates="books")
    # Relationship with the review model
    reviews : List["Review"] = Relationship(back_populates="book",sa_relationship_kwargs={'lazy':'selectin'})
    tags : List["Tag"] = Relationship(link_model=BookTag,back_populates="books", sa_relationship_kwargs={'lazy':'selectin'})    

    
    # Method that gives a string representation of the book object in our db
    def __repr__(self):
        return f"<Book {self.title}>"
    

    
class Review(SQLModel, table=True):
    __tablename__ = "review"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        ))
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default= None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default= None, foreign_key="books.uid")
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    # Relationship with the user model
    user : Optional["User"] = Relationship(back_populates="reviews")
    # Relationship with the book model
    book : Optional["Book"] = Relationship(back_populates="reviews")
    
    # Method that gives a string representation of the review object in our db
    def __repr__(self) -> str:
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"

class Tag(SQLModel,table=True):
    __tablename__="tags"
    
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        ))
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books : List["Book"] = Relationship(link_model=BookTag,back_populates="tags", sa_relationship_kwargs={'lazy':'selectin'})    
    
    def __repr__(self):
        return f"<Tag {self.name}>"
    
