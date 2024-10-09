
# Dockerfile for FastAPI Project

FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install

COPY . /app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
