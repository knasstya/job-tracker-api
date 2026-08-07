def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Tracker API"
    }


def test_create_job(client, sample_job):
    response = client.post(
        "/jobs/",
        json=sample_job
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Google"
    assert data["position"] == "Backend Developer"
    assert data["status"] == "Applied"


def test_get_jobs(client, sample_job):
    client.post(
        "/jobs/",
        json=sample_job
    )

    response = client.get("/jobs/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_get_job_by_id(client, sample_job):
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


def test_update_job(client, sample_job):
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


def test_delete_job(client, sample_job):
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


def test_get_nonexistent_job(client):
    response = client.get("/jobs/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }

def test_update_nonexistent_job(client):
    response = client.patch(
        "/jobs/9999",
        json={
            "status": "Interview"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }

def test_delete_nonexistent_job(client):
    response = client.delete("/jobs/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }

def test_get_jobs_by_status(client):
    client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Backend Developer"
        }
    )

    interview_response = client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Backend Developer"
        }
    )

    job_id = interview_response.json()["id"]

    client.patch(
        f"/jobs/{job_id}",
        json={
            "status": "Interview"
        }
    )

    response = client.get(
        "/jobs/?status=Interview"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for job in data:
        assert job["status"] == "Interview"

def test_create_job_invalid_status(client):
    response = client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Backend Developer",
            "status": "banana"
        }
    )

    assert response.status_code == 422

def test_get_jobs_with_limit(client, sample_job):
    client.post(
        "/jobs/",
        json=sample_job
    )

    client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Backend Developer"
        }
    )

    response = client.get("/jobs/?limit=1")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

def test_get_jobs_by_status(client, sample_job):
    client.post(
        "/jobs/",
        json=sample_job
    )

    client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Backend Developer",
            "status": "Interview"
        }
    )

    response = client.get(
        "/jobs/?status=Interview"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for job in data:
        assert job["status"] == "Interview"

def test_get_jobs_with_offset(client):
    client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Developer"
        }
    )

    client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Developer"
        }
    )

    response = client.get(
        "/jobs/?limit=1&offset=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Microsoft"