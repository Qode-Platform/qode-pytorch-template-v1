# Built by .github/workflows/deploy.yml (context ., file Dockerfile) and pushed
# to Artifact Registry. Adapted from the fleet's python stack pack.
#
# Deviations from the pack, and why:
#   - CMD runs the job, not a server: this template has no HTTP surface, so the
#     image is a runnable job image. It will never satisfy a $PORT health check.
#   - torch comes from the CPU wheel index; the default PyPI wheel pulls ~2.5GB of
#     CUDA that a CI builder and this registry do not need.

FROM python:3.12-slim AS build
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
COPY requirements.txt ./
RUN python -m venv /venv \
 && /venv/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision \
 && /venv/bin/pip install -r requirements.txt

FROM python:3.12-slim AS runtime
ARG BUILD_ID=""
WORKDIR /app
ENV PATH=/venv/bin:$PATH PYTHONUNBUFFERED=1 PORT=8000 BUILD_ID=$BUILD_ID
RUN useradd -r -u 10001 app
COPY --from=build /venv /venv
COPY --chown=app:app . .
USER app
EXPOSE 8000
CMD ["python", "-m", "src.train", "--config", "configs/default.yaml"]
