# ── Stage 1: instala dependências ────────────────────────────────────────────
FROM python:3.14-slim AS builder

WORKDIR /build

# libpq-dev é necessário para compilar o psycopg2 (driver PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root --no-interaction --no-ansi

# ── Stage 2: imagem final enxuta ─────────────────────────────────────────────
FROM python:3.14-slim

# libpq5 é necessária em runtime para o psycopg2 funcionar
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /build/.venv /app/.venv

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.backend_to_do_list.main:app", "--host", "0.0.0.0", "--port", "8000"]