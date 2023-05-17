from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NlZHVsYSI6IjEwMTI0MzIzNjYiLCJjYWR1Y2lkYWQiOiIyMDIzLTA1LTAyVDE2OjQ3OjEzLjMyOTk3OCJ9.Z18E-R_zoLsW5TPk6NuqBC_7tWH6UheEDVRSsKteuok'


#test_service_packages_db
from ..config.database import create_engine, sessionmaker
from ..models.ubicacion import Base


test_engine = create_engine(
    'sqlite:///./test_database.db',
    connect_args={'check_same_thread':False}
)

TestSessionLocal = sessionmaker(bind=test_engine,expire_on_commit=False)

def get_test_session():
    TestSession = TestSessionLocal()
    try:
        yield TestSession
    finally:
        TestSession.close()

Base.metadata.create_all(test_engine)



