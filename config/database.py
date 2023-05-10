from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
#new features in moment to create base 
from sqlalchemy.orm import registry

#URL_DATABASE = "sqlite:///../database.db database proof"
URL_DATABASE = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWD')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"
engine = create_engine(
    URL_DATABASE,
    connect_args={'check_same_thread':False}
)

SessionLocal = sessionmaker(bind=engine)

mapper_registry = registry()
Base = mapper_registry.generate_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()