# EA Sports FC Match Analytics

A self-hosted tool for capturing your FC/FIFA match statistics: press a hotkey on
the post-match stats screen and a background agent screenshots it, hands it to a
local service that runs OCR, and (eventually) stores the numbers so you can
browse your history.

**Status: early stage.** The capture path works end to end; the persistence and
analytics layers are not built yet. See [Where this actually is](#where-this-actually-is)
before judging it by the description above.

## Why this exists

I love FIFA (or should I say FC). But EA doesn't give you any real way to track
and analyze your match statistics. Compare that to Dota 2 or League of Legends,
which have genuinely good analytics platforms.

What I want is to track my match performances without manually copying numbers
into a spreadsheet after every game. The focus is Online Seasons, which is what I
play. Hit a hotkey when the match ends, and the system captures the stats and
files them away for later.

If EA ever ships a proper analytics platform for FC, I'll be the first to switch.
Until then, this is also a decent excuse to learn about OCR pipelines and
self-hosted web services.

## How it works

```
  post-match stats screen
           │
           │  Win + O
           ▼
  ┌─────────────────────────────────────────────────┐
  │  agent/  — Windows system-tray app (pystray)    │
  │                                                 │
  │   HotkeyListener ──► screenshot ──► queue.Queue │
  │                                        │        │
  │                       one worker thread│        │
  │                                        ▼        │
  │                                   OCRRunner     │
  └────────────────────────────────────────┬────────┘
                                           │ POST /api/v1/ocr/{type}/{path}
                                           ▼
  ┌─────────────────────────────────────────────────┐
  │  backend/  — FastAPI service (localhost:8000)   │
  │                                                 │
  │   PaddleOCR engine ──► extracted text           │
  │                              │                  │
  │                              ✗ NOT PERSISTED    │
  │                                                 │
  │   SQLite (template's user/item tables only)     │
  │   Dashboard (template's CRUD UI, not match data)│
  └─────────────────────────────────────────────────┘
```

The queue exists so the hotkey callback returns immediately instead of blocking
the UI thread while OCR runs. It is a single-consumer handoff, not a worker pool.

The agent passes a **file path** to the backend rather than the image bytes, so
both halves have to run on the same machine. That is fine for a self-hosted tool
and is why the API is bound to localhost.

## Where this actually is

Being specific, because the diagram above shows intent and the repo shows
reality. As of the last commit (July 2025):

**Works:**

- System-tray agent with a global hotkey (`Win + O`), screenshot capture, and a
  queue plus worker thread feeding the backend.
- A FastAPI route (`/api/v1/ocr/{image_type}/{image_path}`) that loads PaddleOCR
  and runs it against a captured screenshot.
- SQLite as the database backend, swapped in for the template's Postgres.
- OCR proof-of-concept notebooks and FIFA 22 test screenshots under `poc/`.

**Not built yet:**

- **No match-stats schema and no persistence.** There is no `Match` or `Stat`
  model; the OCR route runs the engine and discards the result. This is the next
  piece of work and the biggest gap between this README's opening line and the
  code.
- **No match dashboard.** The web UI is the template's user/item CRUD scaffold.
  The `img/` screenshots in this repo are the template's, not this project's.
- **No stats parsing.** OCR returns text; nothing yet maps it to labelled fields
  (possession, passing, shots).
- **Image type is hardcoded** to `matchfacts-summary` in `agent/main.py`; the
  tab-navigation path for capturing multiple stat screens is stubbed.
- **Tray menu stubs.** "Settings" and "Status: Active" are no-ops.
- Cross-match comparison and trends, a local vision-LLM fallback, and an
  OCR-versus-VLM accuracy benchmark are all ideas, not code.

**Known rough edges:**

- PaddleOCR loads at import, which adds roughly a minute to backend startup.
- `backend/app/core/ocr.py` keeps a module-level dict, which is server-side state
  that shouldn't be there.
- Text filetypes and OCR accuracy are unmeasured; there is no benchmark yet.

## Provenance

This repo was generated from
[fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
(MIT), and much of what you see is that template: the REST API scaffold, auth,
Alembic migrations, the frontend, Docker Compose files, and CI.

**The original work in this project is `agent/` and `poc/`, plus the OCR route
and the SQLite configuration in `backend/`.** Everything else is inherited, and
the commit history reflects the template's, not mine.

## Running it

The backend and the agent run separately, both on the same Windows machine.

```
# backend
cd backend
uv sync
uv run fastapi dev app/main.py      # http://localhost:8000  (first start is slow: PaddleOCR)

# agent, in a second terminal
cd agent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py                      # appears in the system tray
```

Then press `Win + O` on a post-match stats screen. The agent logs to
`fifa_analytics.log`. Note that nothing is stored yet, so there is no match
history to browse — see [Where this actually is](#where-this-actually-is).

See `development.md` for the template's fuller development setup and
`deployment.md` for its Docker deployment story, neither of which this project
needs in its current form.
