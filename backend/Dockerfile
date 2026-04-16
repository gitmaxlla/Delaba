FROM python:3.14-slim-trixie AS development
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
COPY ./pyproject.toml .
COPY ./uv.lock .

RUN uv sync --locked && uv tool install alembic

COPY src ./src
COPY run.py .
COPY alembic.ini .


RUN apt-get update && apt-get install -y curl \
  && rm -rf /var/lib/apt/lists/*

CMD ["uv", "run", "-m", "run"]




FROM python:3.14-slim-trixie AS production
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
COPY ./pyproject.toml .
COPY ./uv.lock .

ENV UV_NO_DEV=1
RUN uv sync --locked && uv tool install uvicorn

COPY src ./src
COPY run.py .

RUN apt-get update && apt-get install -y curl \
  && rm -rf /var/lib/apt/lists/*

CMD ["uv", "run", "run.py"]
