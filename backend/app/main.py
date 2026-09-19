from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine

from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.approval import router as approval_router

from app.logs.logger import (
    log_info,
    log_error,
)




@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        log_info("Starting HobbyFi Copilot")

        ## Creating Database Tables
        Base.metadata.create_all(
            bind=engine
        )

        log_info(
            "Database tables initialized"
        )

    except Exception as e:
        log_error(
            f"Startup error: {str(e)}"
        )

        raise

    yield   ## python keyword that pauses a function and return control to the caller


    ## just for example - 
      #### return ---> stop forever
      #### yield ----> pause now, continue later

    log_info(
        "Shutting down HobbyFi Copilot"
    )


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description=(
        "AI CRM Copilot for HobbyFi vendors"
    ),
    lifespan=lifespan,
)



## for allowing frontend to get response from the backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hobbyfi-copilot-1.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### using include_router to keep project modular and organized
### different endpoints is handled by different files

app.include_router(
    chat_router
)

app.include_router(
    auth_router
)

app.include_router(
    approval_router
)

## Home Page
@app.get("/")
def root():

    return {
        "message": (
            "HobbyFi Copilot API is running"
        )
    }

## Health Check
@app.get("/health")
def health():

    return {
        "status": "healthy",
        "llm_provider": settings.LLM_PROVIDER,
    }