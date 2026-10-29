import json
import os
from urllib.parse import urlparse

from flask import Flask, render_template

app = Flask(__name__)


def _http_url(value):
    """Allow only absolute HTTP(S) links from environment configuration."""
    value = (value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    return value if parsed.scheme in {"http", "https"} and parsed.netloc else ""


def _load_projects():
    raw = os.getenv("PROJECTS_JSON", "").strip()
    if raw:
        try:
            entries = json.loads(raw)
            if isinstance(entries, list):
                projects = []
                for item in entries:
                    if not isinstance(item, dict):
                        continue
                    title = str(item.get("name", "")).strip()
                    if not title:
                        continue
                    projects.append({
                        "name": title,
                        "category": str(item.get("category", "Software")).strip() or "Software",
                        "description": str(item.get("description", "")).strip(),
                        "stack": [
                            str(tag).strip()
                            for tag in item.get("stack", [])
                            if str(tag).strip()
                        ][:5],
                        "demo_url": _http_url(item.get("url")),
                        "repo_url": _http_url(item.get("repo")),
                        "accent": str(item.get("accent", "blue")).strip().lower(),
                    })
                return projects
        except (json.JSONDecodeError, TypeError):
            app.logger.warning("PROJECTS_JSON is invalid; using the built-in project list.")

    return [
        {
            "name": "Digital Read",
            "category": "Education · Digital Library",
            "description": "A pocket-sized digital library connecting readers, creators, teachers, and libraries.",
            "stack": ["Flask", "PostgreSQL", "PWA"],
            "demo_url": _http_url(os.getenv("DIGITAL_READ_URL")),
            "repo_url": _http_url(os.getenv("DIGITAL_READ_REPO_URL")),
            "accent": "blue",
        },
        {
            "name": "Qavzuno",
            "category": "Commerce · Marketplace",
            "description": "An online marketplace designed to help people discover products and shop with confidence.",
            "stack": ["Flask", "PostgreSQL", "Payments"],
            "demo_url": _http_url(os.getenv("QAVZUNO_URL")),
            "repo_url": _http_url(os.getenv("QAVZUNO_REPO_URL")),
            "accent": "orange",
        },
        {
            "name": "ScarZ POS",
            "category": "Business · Point of Sale",
            "description": "A practical point-of-sale experience built to support everyday business operations.",
            "stack": ["Python", "Flask", "PostgreSQL"],
            "demo_url": _http_url(os.getenv("SCARZ_POS_URL")),
            "repo_url": _http_url(os.getenv("SCARZ_POS_REPO_URL")),
            "accent": "violet",
        },
        {
            "name": "Kampala Link Shipping",
            "category": "Logistics · Shipping",
            "description": "A digital front door for air-freight services connecting the United States and Uganda.",
            "stack": ["Python", "Flask", "Web"],
            "demo_url": _http_url(os.getenv("KLS_URL")),
            "repo_url": _http_url(os.getenv("KLS_REPO_URL")),
            "accent": "teal",
        },
    ]


@app.get("/")
def index():
    projects = _load_projects()
    profile = {
        "name": os.getenv("PROFILE_NAME", "Ssempijja Deogratius").strip(),
        "headline": os.getenv(
            "PROFILE_HEADLINE",
            "Software developer building useful digital products.",
        ).strip(),
        "location": os.getenv("PROFILE_LOCATION", "Uganda").strip(),
        "intro": os.getenv(
            "PROFILE_INTRO",
            "I turn practical ideas into thoughtful digital experiences — from education and commerce to business tools and logistics.",
        ).strip(),
        "email": os.getenv("PROFILE_EMAIL", "").strip(),
        "github_url": _http_url(os.getenv("GITHUB_URL", "https://github.com/companyscarz")),
        "linkedin_url": _http_url(os.getenv("LINKEDIN_URL")),
        "website_url": _http_url(os.getenv("PROFILE_WEBSITE_URL")),
        "profile_image_url": _http_url(os.getenv("PROFILE_IMAGE_URL")),
        "logo_url": _http_url(os.getenv("LOGO_URL")),
        "favicon_url": _http_url(os.getenv("FAVICON_URL")),
        "availability": os.getenv("PROFILE_AVAILABILITY", "Open to meaningful opportunities").strip(),
        "about": os.getenv(
            "PROFILE_ABOUT",
            "I enjoy building software that solves real problems. My work spans web applications, digital learning, e-commerce, business tools, and customer-focused platforms. I value practical solutions, steady improvement, and building responsibly.",
        ).strip(),
    }
    return render_template("index.html", profile=profile, projects=projects)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=False)
