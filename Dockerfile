FROM python:3.9.18-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app
COPY entrypoint.sh /app/entrypoint.sh

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]

EXPOSE 8000
