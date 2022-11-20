FROM python:3.9

WORKDIR /app

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

RUN pip install poetry
COPY poetry.* /app/
COPY pyproject.toml .

RUN poetry install

COPY little_conf little_conf
COPY tests tests
