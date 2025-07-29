FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.0.0

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "entrypoint:app", "--host", "0.0.0.0", "--port", "8000"]