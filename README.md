# My Profile

A responsive personal portfolio for **Ssempijja Deogratius**, built with Flask and server-rendered HTML. Profile details, branding, contact links, and project URLs can be configured through environment variables.

## Features

- Responsive portfolio layout with About, Projects, Skills, Approach, and Contact sections.
- Project cards show live demos and source repositories when links are configured.
- Optional profile photo, logo, and favicon via public HTTP(S) URLs.
- Project list can be customized with `PROJECTS_JSON`.
- Basic health endpoint at `/health`.
- URL validation for configured external links.
- Initial automated tests.

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

The app starts on **port 8000 by default** (`http://127.0.0.1:8000`). Set `PORT` to override it. Copy `.env.example` to `.env` and adjust the values for local development; `python-dotenv` loads `.env` automatically. Do not commit `.env` or put secrets in it.

## Environment configuration

See [`.env.example`](.env.example) for settings, including profile text, contact details, social links, and image URLs. Project demo links and repository links can be set with `DIGITAL_READ_URL`, `QAVZUNO_URL`, `SCARZ_POS_URL`, `KLS_URL`, and the matching `*_REPO_URL` variables.

Set `PROJECTS_JSON` to a JSON array to replace the built-in project list. Each object supports `name`, `category`, `description`, `stack`, `url`, `repo`, and `accent`.

Use public HTTPS URLs for image assets. Keep secrets out of source control; this app does not need API keys for its current features. If no image URLs are provided, the site uses a text monogram and initials.

## Tests

```bash
pip install pytest
pytest -q
```

## Deployment

The repository includes a `Procfile` for platforms that support it:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
```

For Dokploy, connect this repository and deploy it as a Python/Nixpacks application. Configure environment variables in the application settings, set the health check path to `/health` if supported, and use the generated HTTPS URL or your custom domain.

## Development workflow

Develop on `pre-main`. Review and test changes there before merging or deploying production changes from `main`.
