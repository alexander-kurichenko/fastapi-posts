from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#DATABASES = {
#'default': {
#    'ENGINE': '......',
#    'NAME': config('DB_NAME'),
#    'USER': config('DB_USER'),
#    'PASSWORD': config('DB_PASSWORD'),
#    'HOST': config('DB_HOST'),
#    'PORT': 'DB_PORT',
#}

SQLALCHEMY_DATABASE_URL = f"{settings.db_type}://{settings.db_user}:{settings.db_password}@" \
                          f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

