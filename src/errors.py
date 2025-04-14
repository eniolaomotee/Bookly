from typing import Any,Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI,status
from sqlalchemy.exc import SQLAlchemyError

class BooklyException(Exception):
    """Base class for all exceptions in the Bookly application."""
    pass

class InvalidToken(BooklyException):
    """User has provided an Invalid or expired token"""
    pass

class RevokedToken(BooklyException):
    """User has provided a token that has been revoked """
    pass

class AccessTokenRequired(BooklyException):
    """User has not provided a refresh token when an access token is needed"""
    pass

class RefreshTokenRequired(BooklyException):
    """User has not provided a refresh token when a refresh token is needed"""
    pass

class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who exists during sign up."""
    pass

class InvalidCredentials(BooklyException):
    """User has provided a wrong email or password during login."""
    pass
 
class InsufficientPermissions(BooklyException):
    """User does not have the required permissions to perform an action."""
    pass

class BookNotFound(BooklyException):
    """Book not found in the database."""
    pass

class TagNotFound(BooklyException):
    """Tag not found in the database."""
    pass

class TagAlreadyExists(BooklyException):
    """Tag already exists in the database."""
    pass

class UserNotFound(BooklyException):
    """User not found in the database."""
    pass

class AccountNotVerified(BooklyException):
    """User account is not verified."""
    pass

class InvalidPassword(BooklyException):
    """User has provided an invalid password."""
    pass

class ReviewNotFound(BooklyException):
    """Review not found in the database."""
    pass

def create_exception_handler(status_code:int, initial_detail:Any) -> Callable[[Request,Exception], JSONResponse]:
    
    async def exception_handler(request:Request, exc:BooklyException):
        
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
        
    return exception_handler




def register_all_errors(app:FastAPI):
    """Register all custom error handlers with the FastAPI app."""
    app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message":"User with email already exists",
            "error_code":"user_exists"
        }
    )
)

    app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message":"User not found",
            "error_code":"user_not_found"
        }
    )
)


    app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message":"Book not found",
            "error_code":"book_not_found"
        }
    )
)


    app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail={
            "message":"Invalid Email Or Password",
            "error_code":"invalid_email_or_password"
        }
    )
)

    app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message":"Token is invalid or expired",
            "resolution":"Please get a new token",
            "error_code":"invalid_token"
        }
    )
)

    app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message":"Token is invalid or has been revoked",
            "resolution":"Please get a new token",
            "error_code":"token_revoked"
        }
    )
)


    app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message":"Please provide a valid access token",
            "resolution":"Please get an access token",
            "error_code":"access_token_required"
        }
    )
)

    app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message":"Please provide a valid refresh token",
            "resolution":"Please get an refresh token",
            "error_code":"refresh_token_required"
        }
    )
)


    app.add_exception_handler(
    InsufficientPermissions,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message":"You do not have the enough permissions to perform this action",
            "error_code":"insufficient_permission"
        }
    )
)

    app.add_exception_handler(
    TagNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message":"Tag not found",
            "error_code":"tag_not_found"
        }
    )
)


    app.add_exception_handler(
    TagAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message":"Tag already exists",
            "error_code":"tag_exists"
        }
    )
)


    app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message":"Book Not Found",
            "error_code":"book_not_found"
        }
    )
)
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message":"Account not verified",
                "resolution":"Please check your email for verification details",
                "error_code":"account_not_verified"
            }
        )
    )
    
    app.add_exception_handler(
        InvalidPassword,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message":"Passwords do not match",
                "resolution":"Please check your passwords and try again",
                "error_code":"password_mismatch"
            }
        )
    )
    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message":"Review not found",
                "resolution":"Please crosscheck for the review",
                "error_code":"review_not_found"
            }
        )
    )
    
    


    @app.exception_handler(500)
    async def internal_server_error(request,exc):
     return JSONResponse(
            content={"messsgae":"Oops! Something went wrong","error_code":"internal_server_error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        