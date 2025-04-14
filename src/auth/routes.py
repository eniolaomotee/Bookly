from fastapi import APIRouter, Depends, HTTPException,status
from .schemas import UserCreate, UserModel, UserLoginModel, UserBooksModel,EmailModel, PasswordResetRequestModel,PasswordResetConfirm
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.db import get_session  
from .service import UserService
from .utils import create_access_token,decode_token,verify_password, create_url_safe_token,decode_url_safe_token,generate_password_hash
from datetime import timedelta
from src.config import Config
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer,AccessTokenBearer,get_current_user, RoleChecker
from datetime import datetime
from src.db.redis import add_jti_to_blocklist
from src.errors import (UserAlreadyExists,UserNotFound,InvalidCredentials,InvalidToken,InvalidPassword)
from src.mail import mail,create_message
from src.config import Config
from src.db.db import get_session

auth_router = APIRouter()

user_service = UserService()

role_checker = Depends(RoleChecker(['admin','user']))

REFRESH_TOKEN_EXPIRY=2


@auth_router.post("/send_mail")
async def send_mail(emails:EmailModel):
    emails = emails.addresses
    
    html = "<h1>Welcome to the App</h1>"

    message = create_message(
        recipients=emails,
        subject="Welcome to Bookly",
        body=html
    )
    
    await mail.send_message(message)
    
    return {"message":"Email sent successfully"}





@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    
    """ Create a new user account using email,username, first_name, last_name
    params:
    user_data: UserCreate
        The user data to create a new account.
    """
    email = user_data.email
    
    user_exists = await user_service.user_exists(email,session)
    
    if user_exists:
        raise UserAlreadyExists()
    
    new_user = await user_service.create_user(user_data,session)
    
    token = create_url_safe_token({"email":email})
    
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    
    html_message = f"""
    <h1>Verify your Email </h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    
    """
    
    
    message = create_message(
        recipients=[email],
        subject="Verify your Email",
        body=html_message
    )
    
    await mail.send_message(message)
    
    return {
        "message":"Account Created Successfully! Check your email to verify your account",
        "user":new_user
    }
    
@auth_router.get("/verify/{token}")
async def verify_user_account(token:str, session: AsyncSession = Depends(get_session)):
    """ Verify a user account using the token sent to the user's email"""
    token_data = decode_url_safe_token(token)
    
    user_email = token_data.get('email')
    
    if user_email:
        user = await user_service.get_user_by_email(user_email,session)
        
        if not user:
            raise UserNotFound()
        
        await user_service.update_user(user,{"is_verified":True},session)
        
        return JSONResponse(
            content={"message":"Account verified successfully!"},
            status_code=status.HTTP_200_OK
        )
        
    return JSONResponse(
        content={"message":"Error occurred while verifying your account"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        
        )



@auth_router.post("/login")
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    """ Login a user using email and password"""
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user_by_email(email,session)
    
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid),
                     "role":user.role
                })

            refresh_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                },
                    refresh=True,
                    expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
                )
        
            return JSONResponse(
                content={
                    "message":"Login Successful",
                    "access_token":access_token,
                    "refesh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid": str(user.uid)
                    }
                }
            )
            
    raise InvalidCredentials()
    
    
# generate new access token
@auth_router.get("/refresh-token")
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    """ Generate a new access token using the refresh token"""
    expiry_timestamp = token_details['exp']
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        
        return JSONResponse(content={
            "access_token":new_access_token,
        })
    
    raise InvalidToken()


@auth_router.get('/me', response_model=UserBooksModel, dependencies=[role_checker])
async def get_current_user(user = Depends(get_current_user)):
    """ Get the current user using the access token"""
    return user
    

@auth_router.get('/logout')
async def revooke_token(token_details: dict = Depends(AccessTokenBearer())):
    """ Revoke the access token using the jti"""
    jti = token_details['jti']
    
    await add_jti_to_blocklist(jti)
    
    return JSONResponse(
        content={
            "message":"Logged out Successfully"
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.post("/password-rest-request")
async def password_reset_request(email_data:PasswordResetRequestModel,session: AsyncSession = Depends(get_session)):
    email = email_data.email
    
    token = create_url_safe_token({"email":email})

    link = f"http: //{Config.DOMAIN}/api/v1/auth/passwird-reset-confirm/{token}"
    
    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset your password</p>
    """
    
    message = create_message(recipients=[email],subject="Password Reset",body=html_message)
    
    await mail.send_message(message)
    
    return JSONResponse(
        content={
            "message":"Please check your email to reset your password"
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.get("/passwird-reset-confirm/{token}")
async def reset_account_password(token:str,passwords:PasswordResetConfirm, session: AsyncSession = Depends(get_session)):
    """ Reset the user password using the token sent to the user's email""" 
    
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password
    
    if new_password != confirm_password:
        raise InvalidPassword()
    
    token_data = decode_url_safe_token(token)
    
    user_email = token_data.get('email')
    
    if user_email:
        user = await user_service.get_user_by_email(user_email,session)
        
        if not user:
            raise UserNotFound()
        
        
        password_hash = generate_password_hash(new_password)
        await user_service.update_user(user,{"password":password_hash},session)
        
        return JSONResponse(
            content={"message":"Password Reset Successfully!"},
            status_code=status.HTTP_200_OK
        )
        
    return JSONResponse(
        content={"message":"Error occurred during password reset"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        
        )



# redis-server
# redis-cli