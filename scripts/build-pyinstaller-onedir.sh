#!/usr/bin/env bash
# Build the PyInstaller onedir release locally and verify the resulting archive.
# Mirrors the `build-pyinstaller-onedir` CI job in .github/workflows/build.yml
# so you can iterate without pushing.
#
# Usage:
#   scripts/build-pyinstaller-onedir.sh                # full pipeline
#   scripts/build-pyinstaller-onedir.sh --skip-nuitka  # reuse existing .so files
#   scripts/build-pyinstaller-onedir.sh --tag=2.1.6    # set version in archive name
#   scripts/build-pyinstaller-onedir.sh --keep         # leave the extracted tree for inspection
#
# Steps:
#   1. Back up premium .py source
#   2. Compile premium modules with Nuitka (unless --skip-nuitka)
#   3. Build onedir with PyInstaller (`pyinstaller swingmusic.spec -- --onedir`)
#   4. Verify --test-pro-imports against the built binary
#   5. Rename inner binary to plain `swingmusic`
#   6. Package as dist/swingmusic-v<tag>-<platform>-<arch>.tar.gz
#   7. Extract to a temp dir and re-run --test-pro-imports + --help against the
#      extracted binary (proves the archive is self-contained)
#   8. Restore premium .py source and clean up

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

SKIP_NUITKA=false
TAG="0.0.0-dev"
KEEP=false
for arg in "$@"; do
    case "$arg" in
        --skip-nuitka) SKIP_NUITKA=true ;;
        --keep) KEEP=true ;;
        --tag=*) TAG="${arg#--tag=}" ;;
        *)
            echo "unknown arg: $arg" >&2
            exit 2
            ;;
    esac
done

PREMIUM_DIR="src/swingmusic/premium"
BACKUP_DIR=".premium-backup"
TMP_EXTRACT=""

backup_premium() {
    echo "==> Backing up premium source files..."
    rm -rf "$BACKUP_DIR"
    mkdir -p "$BACKUP_DIR/recipes"
    for py in "$PREMIUM_DIR"/*.py; do
        [ "$(basename "$py")" = "__init__.py" ] && continue
        cp "$py" "$BACKUP_DIR/"
    done
    for py in "$PREMIUM_DIR"/recipes/*.py; do
        [ "$(basename "$py")" = "__init__.py" ] && continue
        cp "$py" "$BACKUP_DIR/recipes/"
    done
}

restore_premium() {
    [ -d "$BACKUP_DIR" ] || return 0
    echo "==> Restoring premium source files..."
    find "$PREMIUM_DIR" \( -name '*.so' -o -name '*.pyd' \) -delete 2>/dev/null || true
    for py in "$BACKUP_DIR"/*.py; do
        [ -f "$py" ] && cp "$py" "$PREMIUM_DIR/"
    done
    for py in "$BACKUP_DIR"/recipes/*.py; do
        [ -f "$py" ] && cp "$py" "$PREMIUM_DIR/recipes/"
    done
    rm -rf "$BACKUP_DIR"
}

cleanup() {
    restore_premium
    if [ "$KEEP" = false ] && [ -n "$TMP_EXTRACT" ] && [ -d "$TMP_EXTRACT" ]; then
        rm -rf "$TMP_EXTRACT"
    fi
}
trap cleanup EXIT

# --------------------------------------------------------------------
# 1-2. Compile premium
# --------------------------------------------------------------------
if [ "$SKIP_NUITKA" = false ]; then
    backup_premium
    echo "==> Compiling premium modules..."
    bash scripts/compile-premium-modules.sh --uv
else
    echo "==> Skipping premium compilation (--skip-nuitka)"
fi

# --------------------------------------------------------------------
# 3. Build onedir
# --------------------------------------------------------------------
echo "==> Installing package in venv..."
uv run pip install -e .[build] --quiet

echo "==> Running PyInstaller in onedir mode..."
# `--noconfirm` is a PyInstaller flag (overwrite dist/ without prompting).
# Args after `--` are forwarded to the spec file's argparse.
uv run pyinstaller swingmusic.spec --noconfirm -- --onedir

# --------------------------------------------------------------------
# 4. Verify premium against the freshly-built binary
# --------------------------------------------------------------------
inner=$(ls dist/swingmusic/swingmusic_* 2>/dev/null | head -n1 || true)
if [ -z "$inner" ]; then
    echo "FAIL: no swingmusic_* binary in dist/swingmusic/" >&2
    ls -la dist/swingmusic/ >&2 || true
    exit 1
fi
chmod +x "$inner"

echo "==> Verifying premium modules in built binary..."
"$inner" --test-pro-imports

# --------------------------------------------------------------------
# 5. Rename inner binary so the extracted tree is tidy
# --------------------------------------------------------------------
case "$inner" in
    *.exe) mv "$inner" dist/swingmusic/swingmusic.exe ;;
    *)     mv "$inner" dist/swingmusic/swingmusic ;;
esac

# --------------------------------------------------------------------
# 6. Archive (matches CI naming exactly)
# --------------------------------------------------------------------
platform=$(uname -s | tr '[:upper:]' '[:lower:]')
arch=$(uname -m | tr '[:upper:]' '[:lower:]')
case "$platform" in
    mingw*|msys*|cygwin*) platform=windows ;;
esac
out="swingmusic-v${TAG}-${platform}-${arch}"

if [ "$platform" = "windows" ]; then
    archive="dist/${out}.zip"
    echo "==> Packaging as ${archive}..."
    (cd dist && 7z a -tzip "${out}.zip" swingmusic >/dev/null)
else
    archive="dist/${out}.tar.gz"
    echo "==> Packaging as ${archive}..."
    (cd dist && tar -czf "${out}.tar.gz" swingmusic)
fi

# --------------------------------------------------------------------
# 7. Extract to a temp dir and smoke-test the archive end-to-end
# --------------------------------------------------------------------
TMP_EXTRACT=$(mktemp -d)
echo "==> Extracting archive to $TMP_EXTRACT for smoke test..."

if [ "$platform" = "windows" ]; then
    (cd "$TMP_EXTRACT" && 7z x "$OLDPWD/$archive" >/dev/null)
    extracted_bin="$TMP_EXTRACT/swingmusic/swingmusic.exe"
else
    tar -xzf "$archive" -C "$TMP_EXTRACT"
    extracted_bin="$TMP_EXTRACT/swingmusic/swingmusic"
fi

if [ ! -x "$extracted_bin" ]; then
    echo "FAIL: extracted binary missing or not executable: $extracted_bin" >&2
    ls -la "$TMP_EXTRACT/swingmusic/" >&2 || true
    exit 1
fi

echo "==> Running --help on extracted binary..."
"$extracted_bin" --help >/dev/null && echo "    ✓ --help OK"

echo "==> Running --test-pro-imports on extracted binary..."
"$extracted_bin" --test-pro-imports && echo "    ✓ premium imports OK"

# --------------------------------------------------------------------
# Done
# --------------------------------------------------------------------
echo ""
echo "==> All checks passed."
echo "    Archive:   $archive ($(du -h "$archive" | cut -f1))"
if [ "$KEEP" = true ]; then
    echo "    Extracted: $TMP_EXTRACT (kept for inspection — delete manually)"
    TMP_EXTRACT=""  # prevent cleanup trap from removing it
fi
