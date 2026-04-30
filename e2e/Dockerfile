FROM mcr.microsoft.com/playwright/python:v1.58.0-noble

WORKDIR /tests

COPY ./ ./
RUN pip install --no-cache-dir -r test-requirements.txt

ENV PYTHONUNBUFFERED=1
CMD ["pytest", "-s"]
