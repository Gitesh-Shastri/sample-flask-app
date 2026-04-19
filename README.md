# sample-flask-app

A minimal Flask task-list REST API used as a **demo target** for [ShipReady / production-ready-buddy](https://github.com/giteshshastri/ThinkForge/tree/main/production-ready-buddy).

## Purpose

This repo is **intentionally missing** several production-readiness features so you can demo the ShipReady analysis, auto-fix, and AWS ECS deployment pipeline:

| Gap | Impact |
|-----|--------|
| No `Dockerfile` | Cannot containerise / deploy |
| No CI pipeline | No automated quality gates |
| No tests | Zero confidence in changes |
| Hard-coded `SECRET_KEY` | Security vulnerability |
| No `/health` endpoint | Load-balancer health checks will fail |
| `debug=True` always on | Exposes stack traces in production |
| No input validation | API crashes on bad input |
| No structured logging | Impossible to debug in production |

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

API is available at `http://localhost:5000/tasks`.

## Try it with ShipReady

1. Push this repo to GitHub
2. Open ShipReady → **Connect Repo** → paste the GitHub URL
3. Run **AI Analysis** — score will be low (~30-40/100)
4. Click **Apply All Fixes** → GitHub PR is created with Dockerfile, CI pipeline, tests, and more
5. Click **Deploy to AWS ECS** → service goes live on Fargate
