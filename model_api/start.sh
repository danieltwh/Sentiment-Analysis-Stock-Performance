#/bin/sh
# gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:=5000}
uvicorn main:app --host 0.0.0.0 --port 5000 