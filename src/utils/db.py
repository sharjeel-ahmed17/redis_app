from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from src.utils.settings import settings
Base = declarative_base()
engine = create_engine(
    settings.DB_URI , 
    pool_pre_ping=True, 
    pool_recycle=1800
    )

local_session = sessionmaker(bind=engine)


def get_db():
    session = local_session()
    try: 
        yield session
    finally: 
        session.close()