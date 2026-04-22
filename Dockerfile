FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE CHANGELOG.md ./
COPY src/ src/
COPY preload/ preload/
COPY hosted/ hosted/

RUN pip install --no-cache-dir . uvicorn[standard]

ENV PORT=8080
EXPOSE 8080

CMD ["python", "-m", "librarian_mcp.hosted"]
