from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Tracker API"
    }


def test_create_job(sample_job):
    response = client.post(
        "/jobs/",
        json=sample_job
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Google"
    assert data["position"] == "Backend Developer"
    assert data["status"] == "Applied"

def test_get_jobs():
    response = client.get("/jobs/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

def test_get_job_by_id(sample_job):
    create_response = client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = client.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["company"] == "Google"

def test_update_job(sample_job):
    create_response = client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = client.patch(
        f"/jobs/{job_id}",
        json={
            "status": "Interview"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["status"] == "Interview"

def test_delete_job(sample_job):
    create_response = client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = client.delete(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/jobs/{job_id}"
    )

    assert get_response.status_code == 404