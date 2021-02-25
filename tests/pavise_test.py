from pavise.pavise import app, init_db
from pathlib import Path

def test_index():
    tester = app.test_client()
    response = tester.get("/", content_type="html/text")

    assert response.status_code == 200
    assert response.data == b"<h1>Welcome to Pavise</h1><p>This is a test to make sure things are working.</p>"


def test_existence_of_database():
    init_db()
    assert Path("pavise.db").is_file()