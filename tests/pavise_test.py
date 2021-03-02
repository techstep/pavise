from pavise.pavise import create_app, init_db, populate_db
from pathlib import Path
import json
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


def test_populate_test_data():
    added_records = populate_db(app)
    assert added_records == 29


def test_if_url_is_malware():
    url = "http://127.0.0.1:5000/urlinfo/1/www.quiescentlyfrozenmalware.org/test?variable=stuff&variable2=things"
    tester = app.test_client()
    response = tester.get(url)

    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["is_malware"] == True
    