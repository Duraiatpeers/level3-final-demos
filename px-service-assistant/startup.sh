#!/bin/bash
# Azure App Service startup command. One worker so sessions and embeddings stay in one process.
gunicorn -k uvicorn.workers.UvicornWorker -w 1 --timeout 120 -b 0.0.0.0:${PORT:-8000} app.main:app
