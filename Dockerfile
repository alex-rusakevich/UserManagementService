FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-dev
RUN poetry install --no-root --only test

ADD ./src /app/code
WORKDIR /app/code
ENV PYTHONPATH=/app/code
