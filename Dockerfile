# syntax=docker/dockerfile:1.6
#
# Multi-stage Swing Music image.
#
# Stage 1 (compiler) compiles premium Python modules into native extensions.
# Cached when src/swingmusic/premium/ is unchanged — non-premium edits skip
# the slow Nuitka pass entirely.
#
# Stage 2 (builder) assembles the full source tree (with compiled premium
# artifacts swapped in for their .py originals) and produces a wheel.
#
# Stage 3 (runtime) is a slim image carrying only ffmpeg/libev and the
# installed wheel. Premium .py source never reaches it.

ARG PYTHON_VERSION=3.11

############################
# Stage 1 — compiler
############################
FROM python:${PYTHON_VERSION}-slim AS compiler

WORKDIR /build

# C toolchain + ccache for Nuitka's intermediate object cache.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        patchelf \
        ccache \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# /usr/lib/ccache shadows gcc/g++ with ccache wrappers transparently.
ENV PATH="/usr/lib/ccache:${PATH}"

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install nuitka

# Only the premium sources affect this stage. Any change to non-premium
# code leaves this layer cached, skipping Nuitka entirely on rebuilds.
COPY scripts/compile-premium-modules.sh ./scripts/
COPY src/swingmusic/premium/ ./src/swingmusic/premium/

RUN --mount=type=cache,target=/root/.cache/ccache,sharing=locked \
    --mount=type=cache,target=/root/.cache/Nuitka,sharing=locked \
    CCACHE_DIR=/root/.cache/ccache bash scripts/compile-premium-modules.sh

############################
# Stage 2 — builder
############################
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /src

# The release workflow passes --build-arg app_version=<tag>. Export it as
# SETUPTOOLS_SCM_PRETEND_VERSION so the wheel's metadata carries the real
# version; without this, setuptools-scm can't see a git tag in the Docker
# build context and bakes "0.0.0" into METADATA.
ARG app_version=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${app_version}

# Build backend deps. --no-build-isolation in the wheel command below
# means we use this env directly instead of spinning up an isolated venv
# for every rebuild — saves ~15-20s per build.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install setuptools setuptools-scm

COPY pyproject.toml requirements.txt version.txt README.md ./
COPY scripts/ ./scripts/
COPY src/ ./src/

# Replace premium .py sources with the .so artifacts from the compiler
# stage. Premium source never enters the wheel — only compiled object code.
RUN find src/swingmusic/premium -name "*.py" ! -name "__init__.py" -delete
COPY --from=compiler /build/src/swingmusic/premium/ ./src/swingmusic/premium/

RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel . --no-deps --no-build-isolation -w /wheels

############################
# Stage 3 — runtime
############################
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

LABEL "author"="Swing Music"
EXPOSE 1970/tcp
VOLUME /music
VOLUME /config

# Make /music the apparent home directory inside the container so $home
# resolves to it across the app: onboarding userHome, dir-browser default,
# rootDirs="$home" scans, watchdog, and stream auth all pivot to /music.
# Config and logs are insulated because the entrypoint passes --config /config.
ENV HOME=/music

# Redirect backup output (backup_and_restore.py writes to ~/swingmusic.backup)
# into the persistent /config volume — otherwise backups would land inside
# the user's mounted music library at /music/swingmusic.backup.
RUN mkdir -p /config/backups /music && ln -sfn /config/backups /music/swingmusic.backup

# Secondary affordance: surface /music as a clickable entry under /root in
# the dir-browser, in case HOME resolution is bypassed somewhere.
RUN ln -sfn /music /root/music

# Runtime system packages only.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libev-dev \
        ffmpeg \
        libavcodec-extra && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Fallback for swingmusic/api/settings.py when Metadata.version == "0.0.0"
# (e.g. when app_version build arg is not supplied). Opened relative to
# WORKDIR.
COPY version.txt /app/version.txt

# Install the pre-built wheel from the builder stage. Pip cache mount
# keeps transitive deps (pillow, flask, sqlalchemy, etc.) downloaded
# across rebuilds so this layer is download-free even when invalidated.
COPY --from=builder /wheels/*.whl /tmp/wheels/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install /tmp/wheels/*.whl && \
    rm -rf /tmp/wheels

ENTRYPOINT ["python", "-m", "swingmusic", "--host", "0.0.0.0", "--config", "/config"]
