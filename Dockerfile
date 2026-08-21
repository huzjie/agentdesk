# AgentDesk — multi-stage build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml README.md ./
COPY agentdesk/ ./agentdesk/
RUN pip install --no-cache-dir ".[api]" .

FROM python:3.11-slim AS runtime
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/agentdesk /usr/local/bin/agentdesk
COPY agentdesk/ ./agentdesk/
RUN mkdir -p /app/.agentdesk && chmod 777 /app/.agentdesk
EXPOSE 8500
HEALTHCHECK CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8500/healthz')" || exit 1
CMD ["agentdesk", "serve", "--host", "0.0.0.0", "--port", "8500"]
