# DeviceHub

DeviceHub is a minimal Flask application that shows the service status page.

## Run & Operate

- `python3 app.py` — run DeviceHub on `0.0.0.0` using the configured `PORT` value
- `python3 -m compileall app.py` — check the Python entrypoint syntax
- `python3 -m pip install -r requirements.txt` — install the Flask dependency

## Stack

- Python 3.9+
- Flask

## Where things live

- `app.py` — Flask entrypoint and the single `/` route
- `templates/index.html` — the DeviceHub status page
- `requirements.txt` — Python dependency declaration

## Architecture decisions

- The first version intentionally has no database, authentication, persistence, or REST API.
- Flask serves the status page directly so no frontend build or JavaScript runtime is required.

## Product

The app currently displays the DeviceHub service status message `DeviceHub läuft`.

## User preferences

No additional preferences recorded.

## Gotchas

- The server must bind to `0.0.0.0` and use `PORT` for Replit preview and deployment access.

## Pointers

- Keep future work scoped to the Flask application until database, authentication, or API requirements are explicitly added.
