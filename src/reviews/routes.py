from fastapi import APIRouter, Depends,status
from src.db.models import User
from src.reviews.schemas import ReviewCreateModel,ReviewModel
from src.db.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService
from src.auth.dependencies import get_current_user
from typing import List

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_uid}", status_code=status.HTTP_201_CREATED, response_model=ReviewModel)
async def add_review_to_book(book_uid:str,review_data: ReviewCreateModel,current_user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    new_review = await review_service.add_review_to_book(user_email=current_user.email, review_data=review_data, book_uid=book_uid, session=session)
    
    return new_review

@review_router.get("/",status_code=status.HTTP_200_OK, response_model=List[ReviewModel])
async def get_all_reviews(session: AsyncSession= Depends(get_session)):
    reviews = await review_service.get_all_reviews(session=session)
    return reviews


@review_router.get("/{review_uid}", status_code=status.HTTP_200_OK, response_model=ReviewModel)
async def get_review_by_id(review_uid:str, session:AsyncSession = Depends(get_session)):
    review = await review_service.get_review_by_id(review_uid=review_uid, session=session)
    return review

@review_router.patch("/{review_uid}", response_model=ReviewModel, status_code=status.HTTP_200_OK)
async def update_review(review_uid:str, review_data:ReviewCreateModel, session:AsyncSession = Depends(get_session)):
    updated_review = await review_service.update_review(review_uid=review_uid, review_data=review_data, session=session)
    return updated_review

@review_router.delete("/{review_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_uid:str, session:AsyncSession = Depends(get_session)):
    deleted_review = await review_service.delete_review(review_uid=review_uid, session=session)
    return deleted_review

