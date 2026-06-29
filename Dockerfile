FROM python:3.14 AS builder

WORKDIR /build

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction --no-ansi

FROM python:3.14

WORKDIR /app

COPY --from=builder /build/.venv /app/.venv

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "src.backend_to_do_list.main:app", "--host", "0.0.0.0", "--port", "8000"]