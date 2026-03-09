FROM python:3.14-slim-trixie as DEVELOPMENT
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
COPY ./pyproject.toml .
COPY ./uv.lock .

RUN uv sync --locked
RUN uv tool install uvicorn

COPY src ./src
COPY run.py .

CMD ["uv", "run", "run.py"]


FROM python:3.14-slim-trixie as PRODUCTION
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
COPY ./pyproject.toml .
COPY ./uv.lock .

ENV UV_NO_DEV=1
RUN uv sync --locked
RUN uv tool install uvicorn

COPY src ./src
COPY run.py .

CMD ["uv", "run", "run.py"]
