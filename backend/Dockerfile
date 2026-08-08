# backend/Dockerfile
FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

# Apply latest Debian security updates in the image layer.
RUN apt-get update \
  && apt-get upgrade -y --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

# Install uv (fast, deterministic installs)
RUN pip install --no-cache-dir uv

# Copy dependency files first for better Docker caching
COPY pyproject.toml uv.lock ./

# Install only runtime deps in base
RUN uv sync --frozen --no-dev

# Now copy the application code
COPY . .

# ----------------------------
# Test image: adds dev deps (pytest, etc.)
# ----------------------------
FROM base AS test
RUN uv sync --frozen --group dev

# Default command for this image is running tests
CMD ["uv", "run", "pytest", "--cov=app", "--cov=library", "--cov-report=term-missing", "--cov-fail-under=85"]

# ----------------------------
# Runtime image: what you'd deploy. Starts fresh from the base image rather
# than FROM base, so pip/uv (and their vendored dependencies) are never
# installed here at all — only the already-built /opt/venv is copied in.
# ----------------------------
FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

# Apply latest Debian security updates in the image layer.
RUN apt-get update \
  && apt-get upgrade -y --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

COPY --from=base /opt/venv /opt/venv
COPY --from=base /app /app

# python:3.14-slim ships pip pre-installed. /opt/venv is fully self-contained,
# so nothing at runtime needs it — remove it along with its vendored
# dependencies (e.g. an outdated pip/_vendor/msgpack), which otherwise show
# up in Trivy scans of the shipped image despite never being our own deps.
RUN python -m pip uninstall -y pip

# Create a non-root user
RUN useradd -m -u 10001 appuser

# Switch to non-root
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health').status == 200 else 1)"

CMD ["/opt/venv/bin/uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
