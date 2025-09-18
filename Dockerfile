FROM python:3.12-slim

COPY . /app
WORKDIR /app

ENV PYTHONPATH=/app

ENV PYTHONPATH=/app

COPY pyproject.toml .

RUN pip install -U pip setuptools wheel
RUN pip install zstandard
RUN pip install pdm
RUN pdm install --prod --frozen-lockfile --no-editable

ENTRYPOINT ["pdm", "run", "src/server.py"]
