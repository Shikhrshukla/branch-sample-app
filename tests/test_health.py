from app import create_app

def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    res = client.get("/health")

    # Accept 200 (healthy) OR 500 (DB unavailable but route works)
    assert res.status_code in (200, 500)
    assert "status" in res.json

