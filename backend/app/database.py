from sqlalchemy import create_engine


from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


from app.config import settings

engine_kwargs = {}

if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }


engine = create_engine(

    settings.DATABASE_URL,
    pool_pre_ping=True,
    **engine_kwargs

)





SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)





Base = declarative_base()





def get_db():


    db = SessionLocal()


    try:

        yield db


    finally:

        db.close()