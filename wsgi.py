import os
from pavise.pavise import create_app

app = create_app(os.environ["FLASK_CONFIG"])