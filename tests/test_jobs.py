def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Tracker API"
    }


def test_create_job(authenticated_client, sample_job):
    response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Google"
    assert data["position"] == "Backend Developer"
    assert data["status"] == "Applied"


def test_get_jobs(authenticated_client, sample_job):
    authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    response = authenticated_client.get("/jobs/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_get_job_by_id(authenticated_client, sample_job):
    create_response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = authenticated_client.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["company"] == "Google"


def test_update_job(authenticated_client, sample_job):
    create_response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/jobs/{job_id}",
        json={
            "status": "Interview"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["status"] == "Interview"


def test_delete_job(authenticated_client, sample_job):
    create_response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = authenticated_client.delete(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 204

    get_response = authenticated_client.get(
        f"/jobs/{job_id}"
    )

    assert get_response.status_code == 404


def test_get_nonexistent_job(authenticated_client):
    response = authenticated_client.get("/jobs/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }

def test_update_nonexistent_job(authenticated_client):
    response = authenticated_client.patch(
        "/jobs/9999",
        json={
            "status": "Interview"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }

def test_delete_nonexistent_job(authenticated_client):
    response = authenticated_client.delete("/jobs/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }

def test_get_jobs_by_status(authenticated_client):
    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Backend Developer"
        }
    )

    interview_response = authenticated_client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Backend Developer"
        }
    )

    job_id = interview_response.json()["id"]

    authenticated_client.patch(
        f"/jobs/{job_id}",
        json={
            "status": "Interview"
        }
    )

    response = authenticated_client.get(
        "/jobs/?status=Interview"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for job in data:
        assert job["status"] == "Interview"

def test_create_job_invalid_status(authenticated_client):
    response = authenticated_client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Backend Developer",
            "status": "banana"
        }
    )

    assert response.status_code == 422

def test_get_jobs_with_limit(authenticated_client, sample_job):
    authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Backend Developer"
        }
    )

    response = authenticated_client.get("/jobs/?limit=1")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

def test_get_jobs_by_status_with_sample_job(authenticated_client, sample_job):
    authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Backend Developer",
            "status": "Interview"
        }
    )

    response = authenticated_client.get(
        "/jobs/?status=Interview"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for job in data:
        assert job["status"] == "Interview"

def test_get_jobs_with_offset(authenticated_client):
    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Developer"
        }
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Developer"
        }
    )

    response = authenticated_client.get(
        "/jobs/?limit=1&offset=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Google"


def test_get_jobs_invalid_limit(authenticated_client):
    response = authenticated_client.get(
        "/jobs/?limit=0"
    )

    assert response.status_code == 422


def test_get_jobs_invalid_offset(authenticated_client):
    response = authenticated_client.get(
        "/jobs/?offset=-1"
    )

    assert response.status_code == 422

def test_get_jobs_sorted_by_company_ascending(
    authenticated_client
):
    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Developer"
        }
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Developer"
        }
    )

    response = authenticated_client.get(
        "/jobs/?sort_by=company&order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]["company"] == "Amazon"
    assert data[1]["company"] == "Microsoft"


def test_get_jobs_sorted_by_company_descending(
    authenticated_client
):
    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Developer"
        }
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Developer"
        }
    )

    response = authenticated_client.get(
        "/jobs/?sort_by=company&order=desc"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]["company"] == "Microsoft"
    assert data[1]["company"] == "Amazon"


def test_get_jobs_invalid_sort_field(
    authenticated_client
):
    response = authenticated_client.get(
        "/jobs/?sort_by=banana"
    )

    assert response.status_code == 422


def test_get_jobs_invalid_sort_order(
    authenticated_client
):
    response = authenticated_client.get(
        "/jobs/?order=banana"
    )

    assert response.status_code == 422

def test_user_cannot_access_another_users_job(
    create_authenticated_client
):
    user_a = create_authenticated_client(
        "user_a@example.com"
    )

    user_b = create_authenticated_client(
        "user_b@example.com"
    )

    response = user_a.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Backend Developer"
        }
    )

    assert response.status_code == 201

    job_id = response.json()["id"]

    response = user_a.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200

    response = user_b.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }

def test_user_cannot_update_another_users_job(
    create_authenticated_client
):
    user_a = create_authenticated_client(
        "user_a@example.com"
    )

    user_b = create_authenticated_client(
        "user_b@example.com"
    )

    response = user_a.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Backend Developer"
        }
    )

    assert response.status_code == 201

    job_id = response.json()["id"]

    response = user_b.patch(
        f"/jobs/{job_id}",
        json={
            "status": "Interview"
        }
    )

    assert response.status_code == 404

    response = user_a.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Applied"

def test_user_cannot_delete_another_users_job(
    create_authenticated_client
):
    user_a = create_authenticated_client(
        "user_a@example.com"
    )

    user_b = create_authenticated_client(
        "user_b@example.com"
    )

    response = user_a.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Backend Developer"
        }
    )

    assert response.status_code == 201

    job_id = response.json()["id"]

    response = user_b.delete(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 404

    response = user_a.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200

def test_update_job_company(authenticated_client, sample_job):
    create_response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/jobs/{job_id}",
        json={
            "company": "Microsoft"
        }
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Microsoft"
    assert response.json()["position"] == "Backend Developer"
    assert response.json()["status"] == "Applied"


def test_update_job_position(authenticated_client, sample_job):
    create_response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/jobs/{job_id}",
        json={
            "position": "Senior Backend Developer"
        }
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Google"
    assert response.json()["position"] == "Senior Backend Developer"
    assert response.json()["status"] == "Applied"


def test_update_job_company_and_position(
    authenticated_client,
    sample_job
):
    create_response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/jobs/{job_id}",
        json={
            "company": "Microsoft",
            "position": "Senior Backend Developer"
        }
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Microsoft"
    assert response.json()["position"] == "Senior Backend Developer"
    assert response.json()["status"] == "Applied"


def test_update_job_empty_body(
    authenticated_client,
    sample_job
):
    create_response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/jobs/{job_id}",
        json={}
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Google"
    assert response.json()["position"] == "Backend Developer"
    assert response.json()["status"] == "Applied"

def test_get_jobs_pagination_and_sorting(
    authenticated_client
):
    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Developer"
        }
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Developer"
        }
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "position": "Developer"
        }
    )

    response = authenticated_client.get(
        "/jobs/?sort_by=company&order=asc&limit=1&offset=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Google"


def test_get_jobs_default_sorting(authenticated_client):
    first = authenticated_client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Developer"
        }
    )

    second = authenticated_client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Developer"
        }
    )

    response = authenticated_client.get("/jobs/")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["id"] == second.json()["id"]
    assert data[1]["id"] == first.json()["id"]

def test_get_jobs_sorted_by_position_ascending(
    authenticated_client
):
    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Senior Developer"
        }
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Backend Developer"
        }
    )

    response = authenticated_client.get(
        "/jobs/?sort_by=position&order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]["position"] == "Backend Developer"
    assert data[1]["position"] == "Senior Developer"

def test_get_jobs_sorted_by_position_descending(
    authenticated_client
):
    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Senior Developer"
        }
    )

    authenticated_client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Backend Developer"
        }
    )

    response = authenticated_client.get(
        "/jobs/?sort_by=position&order=desc"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]["position"] == "Senior Developer"
    assert data[1]["position"] == "Backend Developer"

def test_get_jobs_sorted_by_created_at_ascending(
    authenticated_client
):
    first = authenticated_client.post(
        "/jobs/",
        json={
            "company": "Google",
            "position": "Developer"
        }
    )

    second = authenticated_client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "position": "Developer"
        }
    )

    response = authenticated_client.get(
        "/jobs/?sort_by=created_at&order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]["id"] == first.json()["id"]
    assert data[1]["id"] == second.json()["id"]

def test_create_job_missing_required_fields(
    authenticated_client
):
    response = authenticated_client.post(
        "/jobs/",
        json={}
    )

    assert response.status_code == 422

def test_update_job_invalid_status(
    authenticated_client,
    sample_job
):
    create_response = authenticated_client.post(
        "/jobs/",
        json=sample_job
    )

    job_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/jobs/{job_id}",
        json={
            "status": "banana"
        }
    )

    assert response.status_code == 422

    