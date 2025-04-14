from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.schemas import ReviewCreateModel
from fastapi import HTTPException, status
import logging
from src.errors import ReviewNotFound, UserNotFound, BookNotFound
from sqlmodel import select,desc

book_service = BookService()
user_service = UserService()

class ReviewService():
    async def add_review_to_book(self,user_email:str, book_uid:str,review_data: ReviewCreateModel ,session:AsyncSession):
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            user = await user_service.get_user_by_email(email=user_email,session=session)
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)
            
            if not book:
                raise BookNotFound()
            
            if not user:
                raise UserNotFound()
            
            new_review.user = user
            
            new_review.book = book
            
            session.add(new_review)
            
            await session.commit()
            
            return new_review
        
        except Exception as e:
            logging.exception("Error adding review to book: %s", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops something went wrong")
        
    async def get_all_reviews(self, session:AsyncSession):
        statement = select(Review).order_by(Review.created_at.desc())
        
        result = await session.exec(statement)
        
        return result.all()
    
    async def get_review_by_id(self, review_uid:str, session:AsyncSession):
        try:
            review = await session.get(Review, review_uid)
            
            if not review:
                raise ReviewNotFound()
            
            return review
        
        except Exception as e:
            logging.exception("Error fetching review by ID: %s", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops something went wrong")
    
    async def delete_review(self, review_uid:str, session:AsyncSession):
        try:
            review = await session.get(Review, review_uid)
            
            if not review:
                raise ReviewNotFound()
            
            await session.delete(review)
            await session.commit()
            
            return {"message":"Review deleted successfully"}
        
        except Exception as e:
            logging.exception("Error deleting review: %s", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops something went wrong")
        
    async def update_review(self, review_uid:str, review_data:ReviewCreateModel, session:AsyncSession):
        try:
            review = await session.get(Review, review_uid)
            
            if not review:
                raise ReviewNotFound()
            
            update_review_dict = review_data.model_dump()
            
            for k, v in update_review_dict.items():
                setattr(review, k, v)
                
                await session.commit()
                await session.refresh(review)
            
            return review
        
        except Exception as e:
            logging.exception("Error updating review: %s", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops something went wrong")
        
        