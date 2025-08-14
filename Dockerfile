FROM python:3.13-slim

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app

COPY pyproject.toml .

RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libatlas-base-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip setuptools wheel
RUN pip install zstandard pdm
RUN pdm install --prod --frozen-lockfile --no-editable

ENTRYPOINT ["pdm", "run", "src/server.py"]
