#!/bin/bash

sleep 5

alembic upgrade head

gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000