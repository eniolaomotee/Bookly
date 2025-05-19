from fastapi import Header, APIRouter
from typing import Optional

header_router = APIRouter()


@header_router.get("/")
async def get_all_request_headers(
    user_agent:Optional[str] = Header(None),
    accept_encoding:Optional[str] = Header(None),
    referrer:Optional[str] = Header(None),
    connection: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    host: Optional[str] = Header(None),
    cookie: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None),
    x_real_ip: Optional[str] = Header(None),
):
    request_headers = {}
    request_headers['User-Agent'] = user_agent
    request_headers['Accept-Encoding'] = accept_encoding
    request_headers['Referrer'] = referrer
    request_headers['Connection'] = connection
    request_headers['Accept-Language'] = accept_language
    request_headers['Host'] = host
    request_headers['Cookie'] = cookie
    request_headers['Authorization'] = authorization   
    request_headers['X-Forwarded-For'] = x_forwarded_for
    request_headers['X-Real-IP'] = x_real_ip
    
    return request_headers

@header_router.get("/health-check")
async def health_check():
    return {"status":"ok"}