import pytest
import sys
from pathlib import Path

# Add src to path so tests can import from it
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

