FROM python:3.14-slim-trixie

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src .

CMD ["fastapi", "run", "main.py", "--port", "8000"]
