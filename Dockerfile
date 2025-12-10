FROM ghcr.io/astral-sh/uv:python3.14-bookworm AS builder
ENV UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

FROM python:3.14-slim

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

COPY --from=builder --chown=nonroot:nonroot /app /app
COPY --chown=nonroot:nonroot src /app
COPY --chown=nonroot:nonroot .env /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
ENTRYPOINT [ "/bin/bash" ]

EXPOSE 8000
CMD ["python", "main.py"]