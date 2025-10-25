
from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)

def test_root():
    assert c.get('/').status_code==200

def test_predict():
    r=c.post('/predict',json={'text':'you idiot'})
    assert r.status_code==200
    js=r.json()
    assert 'foulness_meter' in js and 0 <= js['foulness_meter'] <= 10
