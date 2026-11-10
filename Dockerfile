
# syntax=docker/dockerfile:1

# ==========================================
# Stage 1: Builder
# ==========================================

FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project
RUN uv sync --frozen --no-dev --no-install-project

# Copy project source
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev


# ==========================================
# Stage 2: Production
# ==========================================

FROM python:3.13-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE="verba.configs.settings"

WORKDIR /app

# Copy virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY --from=builder /app/src /app/src
COPY --from=builder /app/manage.py /app/manage.py

# Create non-root user
RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app

USER app

EXPOSE 80

CMD ["gunicorn", "verba.configs.wsgi:application", "--bind", "0.0.0.0:80", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-"]
