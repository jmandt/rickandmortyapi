FROM python:3.10.0-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt update \
    && apt install -y --no-install-recommends curl git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.1.11 POETRY_HOME=/opt/poetry python3 \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/ \
    && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./deps/
RUN cd ./deps && poetry install --no-root --no-dev && cd .. && rm -rf ./deps

# set working directory
WORKDIR /app
ENV PYTHONPATH /app

COPY app .

ENTRYPOINT exec gunicorn --bind :8080 --workers 1 --threads 4 --timeout 0 main:app -k uvicorn.workers.UvicornWorker
