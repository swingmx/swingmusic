# syntax=docker/dockerfile:1.6
#
# Multi-stage Swing Music image.
#
# Stage 1 (builder) compiles the premium Python modules with Nuitka and
# builds a wheel. Stage 2 (runtime) is a slim image that only contains
# the runtime deps (ffmpeg, libev) and the installed wheel. The .py
# source for premium modules never reaches the runtime stage — only the
# compiled .so extension modules do.

ARG PYTHON_VERSION=3.11

############################
# Stage 1 — builder
############################
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /src

# The release workflow passes --build-arg app_version=<tag>. Export it as
# SETUPTOOLS_SCM_PRETEND_VERSION so the wheel's metadata carries the real
# version; without this, setuptools-scm can't see a git tag in the Docker
# build context and bakes "0.0.0" into METADATA, making Metadata.version
# return "0.0.0" at runtime.
ARG app_version=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${app_version}

# Build deps for Nuitka + native C extensions.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        patchelf \
        libev-dev \
        ccache \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy project sources needed for the wheel build.
COPY pyproject.toml requirements.txt version.txt README.md ./
COPY src/ ./src/
COPY scripts/ ./scripts/

# Install Nuitka and the standard build frontend.
RUN pip install --no-cache-dir nuitka build

# Compile premium modules in place. Produces .so files alongside the
# package and removes the .py sources — everything downstream only sees
# compiled object code.
RUN bash scripts/compile-premium-modules.sh

# Build a wheel containing the compiled premium modules.
RUN python -m build --wheel --outdir /wheels

############################
# Stage 2 — runtime
############################
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

LABEL "author"="Swing Music"
EXPOSE 1970/tcp
VOLUME /music
VOLUME /config

# Runtime system packages only.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libev-dev \
        ffmpeg \
        libavcodec-extra && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the pre-built wheel from the builder stage.
COPY --from=builder /wheels/*.whl /tmp/wheels/
RUN pip install --no-cache-dir /tmp/wheels/*.whl && \
    rm -rf /tmp/wheels

ENTRYPOINT ["python", "-m", "swingmusic", "--host", "0.0.0.0", "--config", "/config"]
