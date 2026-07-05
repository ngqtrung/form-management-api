FROM python:3.8-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.5 \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "alembic upgrade head && python run.py seed && python run.py api --host=0.0.0.0 --no-debug"]
