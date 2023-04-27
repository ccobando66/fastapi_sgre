from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
#new features in moment to create base 
from sqlalchemy.orm import registry

#URL_DATABASE = "sqlite:///../database.db"
URL_DATABASE = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWD')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"
engine = create_engine(
    URL_DATABASE,
    
)

SessionLocal = sessionmaker(
                            autocommit=False,
                            bind=engine,
                            autoflush=False
                            )

mapper_registry = registry()
Base = mapper_registry.generate_base()