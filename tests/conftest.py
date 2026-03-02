import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient and restore global `activities` after each test."""
    # Arrange: snapshot activities state
    original = copy.deepcopy(activities)
    with TestClient(app) as c:
        # Act/Assert: tests will use the client
        yield c
    # Teardown: restore original activities to avoid cross-test mutation
    activities.clear()
    activities.update(original)
