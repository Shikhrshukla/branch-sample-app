from app import create_app

def test_loans_list_route_exists():
    app = create_app()
    client = app.test_client()

    res = client.get("/api/loans")
    # It may return [] or fail if DB missing, but route should exist
    assert res.status_code in (200, 500)

def test_stats_route_exists():
    app = create_app()
    client = app.test_client()

    res = client.get("/api/stats")
    # route should exist even if DB unavailable
    assert res.status_code in (200, 500)
