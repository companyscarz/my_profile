import json

from app import app, _http_url


def test_homepage_renders_profile_and_projects():
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Ssempijja Deogratius" in response.data
    assert b"Digital Read" in response.data
    assert b"Qavzuno" in response.data


def test_health_endpoint():
    app.config["TESTING"] = True
    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_http_url_rejects_non_http_schemes():
    assert _http_url("javascript:alert(1)") == ""
    assert _http_url("https://example.com/path") == "https://example.com/path"


def test_projects_json_can_override_default_list(monkeypatch):
    monkeypatch.setenv(
        "PROJECTS_JSON",
        json.dumps([{
            "name": "Configured project",
            "category": "Demo",
            "description": "Loaded from environment",
            "stack": ["Python"],
            "url": "https://example.com",
            "repo": "https://github.com/example/project",
        }]),
    )
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Configured project" in response.data
    assert b"Digital Read" not in response.data
