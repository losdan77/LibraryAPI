FROM python:3.12

RUN mkdir /api

WORKDIR /api

COPY requeriments.txt .

RUN pip install -r requeriments.txt

COPY . .

RUN chmod a+x /api/docker/*.sh

CMD [ "gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000" ]