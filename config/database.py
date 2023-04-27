from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#new features in moment to create base 
from sqlalchemy.orm import registry

URL_DATABASE = "sqlite:///../database.db"
engine = create_engine(
    URL_DATABASE,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
                            autocommit=False,
                            bind=engine,
                            autoflush=False
                            )

mapper_registry = registry()
Base = mapper_registry.generate_base()