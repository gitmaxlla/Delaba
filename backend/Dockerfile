FROM python:3.14-slim-trixie AS development
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
COPY ./pyproject.toml .
COPY ./uv.lock .

RUN uv sync --locked
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl=8.* && rm -rf /var/lib/apt/lists/*

COPY src ./src
COPY run.py .
COPY alembic.ini .
COPY migrations ./migrations

CMD ["uv", "run", "-m", "run"]


FROM python:3.14-slim-trixie AS production
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
COPY ./pyproject.toml .
COPY ./uv.lock .

ENV UV_NO_DEV=1
RUN uv sync --locked --no-default-groups
# uv tool install uvicorn

COPY src ./src
COPY run.py .
COPY alembic.ini .
COPY migrations ./migrations

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl=8.* && rm -rf /var/lib/apt/lists/*

CMD ["uv", "run", "-m", "run"]
