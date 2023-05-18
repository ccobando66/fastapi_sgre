from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NlZHVsYSI6IjEwMTI0MzIzNjYiLCJjYWR1Y2lkYWQiOiIyMDIzLTA1LTAyVDE2OjQ3OjEzLjMyOTk3OCJ9.Z18E-R_zoLsW5TPk6NuqBC_7tWH6UheEDVRSsKteuok'






