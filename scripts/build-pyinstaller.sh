#!/usr/bin/env bash
# Build a PyInstaller binary with Nuitka-compiled premium modules.
#
# Usage:
#   scripts/build-pyinstaller.sh              # compile premium + build binary
#   scripts/build-pyinstaller.sh --skip-nuitka  # skip premium compilation (use existing .so)
#
# Produces: dist/swingmusic_<os>_<arch>
#
# The script backs up premium .py source before compilation and restores it
# after the PyInstaller build, so your working tree stays clean.

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

SKIP_NUITKA=false
for arg in "$@"; do
    case "$arg" in
        --skip-nuitka) SKIP_NUITKA=true ;;
    esac
done

PREMIUM_DIR="src/swingmusic/premium"
BACKUP_DIR=".premium-backup"

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
    echo "==> Restoring premium source files..."
    # Remove compiled .so/.pyd artifacts
    find "$PREMIUM_DIR" -name '*.so' -o -name '*.pyd' | xargs rm -f 2>/dev/null

    # Restore .py source from backup
    for py in "$BACKUP_DIR"/*.py; do
        [ -f "$py" ] && cp "$py" "$PREMIUM_DIR/"
    done
    for py in "$BACKUP_DIR"/recipes/*.py; do
        [ -f "$py" ] && cp "$py" "$PREMIUM_DIR/recipes/"
    done

    rm -rf "$BACKUP_DIR"
}

# Always restore on exit (success, failure, or interrupt)
trap restore_premium EXIT

# 1. Back up + compile premium modules (unless skipped)
if [ "$SKIP_NUITKA" = false ]; then
    backup_premium
    echo "==> Compiling premium modules..."
    bash scripts/compile-premium-modules.sh --uv
else
    echo "==> Skipping premium compilation (--skip-nuitka)"
fi

# 2. Ensure package + deps are installed (matches CI's `pip install -e .[build]`)
echo "==> Installing package in venv..."
uv run pip install -e .[build] --quiet

# 3. Build with PyInstaller
echo "==> Running PyInstaller..."
uv run pyinstaller swingmusic.spec --noconfirm

echo "==> Done. Binary at:"
ls -lh dist/swingmusic_*
