FROM python:3.12.2-slim

WORKDIR /app

RUN pip install poetry
ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . /app

CMD ["python", "main.py"]
