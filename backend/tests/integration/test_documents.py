import pytest


@pytest.mark.parametrize("get_test_users", ["get_real_db"], indirect=True)
def test_upload_and_download_document(client, mock_admin_auth):
    files = {"file": ("test.pdf", b"%PDF-1.4 test document", "application/pdf")}

    data = {
        "title": "title",
        "subject": "subject",
        "deadline": "2026-01-01",
        "channel": "test",
    }

    response = client.post("/v1/tasks/document", files=files, data=data)
    assert response.status_code == 200

    response = client.get("/v1/tasks/1/file")
    assert response.status_code == 200
    assert response.content == files["file"][1]
