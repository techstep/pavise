from pavise.pavise import create_app, init_db
from pathlib import Path
import os

app = create_app(os.environ["FLASK_CONFIG"])

def test_index():
    tester = app.test_client()
    response = tester.get("/", content_type="html/text")

    assert response.status_code == 200
    assert response.data == b"<h1>Welcome to Pavise</h1><p>This is a test to make sure things are working.</p>"


def test_existence_of_database():
    init_db(app)
    assert Path("pavise.db").is_file()