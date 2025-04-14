from fastapi import FastAPI,status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time 
import logging

# Disable the default Uvicorn access log 
logger = logging.getLogger('uvicorn.access')
logger.disabled = True

def register_middleware(app: FastAPI):
    """
    Register middleware for the FastAPI application.
    """
    @app.middleware('http')
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        
        # Log the request details           
        response = await call_next(request)
        
        processing_time = time.time() - start_time
        
        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time:.2f} seconds"

        print(message)
                
        return response
    
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost","127.0.0.1","https://bookly-api-j8hb.onrender.com"]
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # @app.middleware('http')
    # async def authorization(request:Request, call_next):
    #     """ Middleware to check if the request has an authorization header. """
    #     # Important when using a Middleware you cannot raise an HTTPException inside a Middleware, it would be raised as an exception but it won't be returned as a response.
    #     if not "Authorization" in request.headers:
    #         return JSONResponse(
    #             content={
    #                 "message":"Not Authenticated",
    #                 "resolution":"Please provide the right credentials to proceed"
    #             },
    #             status_code=status.HTTP_401_UNAUTHORIZED
    #         )
            
    #     response = await call_next(request)
        
    #     return response