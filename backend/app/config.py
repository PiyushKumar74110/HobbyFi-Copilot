from pathlib import Path


from pydantic_settings import BaseSettings


BASE_DIR = Path(
    __file__
).resolve().parent.parent.parent





class Settings(
    BaseSettings
):


    # Application

    APP_NAME: str = (
        "HobbyFi Copilot"
    )


    ENVIRONMENT: str = (
        "development"
    )



    # Database

    DATABASE_URL: str



    # LLM


    ## if there is another LLM provider use that else use ollama by default
    
    LLM_PROVIDER: str = (
        "ollama"
    )


    OLLAMA_URL: str = (

        "http://localhost:11434"

    )


    OLLAMA_MODEL: str = (

        "qwen2.5:3b"

    )



    


    # Security

    SECRET_KEY: str



    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60



    # Vector DB

    VECTOR_DB_PATH: str = (
        "vector_db/chroma"
    )



    class Config:


        env_file = (

            BASE_DIR / ".env"

        )





settings = Settings()