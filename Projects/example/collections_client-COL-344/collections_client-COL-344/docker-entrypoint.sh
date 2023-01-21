#!/bin/sh

port=${PORT-8000}
workers=${WORKERS-1}

uvicorn collections_client.main:app --host 0.0.0.0 --workers "$workers" --port "$port"
