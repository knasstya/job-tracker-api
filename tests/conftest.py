import pytest


@pytest.fixture
def sample_job():
    return {
        "company": "Google",
        "position": "Backend Developer"
    }