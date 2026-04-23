#!/usr/bin/env bash
# Compile premium Python modules to native extension modules via Nuitka.
#
# This script walks src/swingmusic/premium/, takes every .py file except
# __init__.py, compiles it with `nuitka --module` (producing a platform-
# specific .so/.pyd), and removes the original .py source. The resulting
# tree is what downstream builds (cibuildwheel, pyinstaller, docker, appimage)
# consume — by the time they run, premium logic exists only as compiled
# object code.
#
# Usage:
#   scripts/compile-premium-modules.sh              # CI (bare python)
#   scripts/compile-premium-modules.sh --uv         # local (uv run python)
#
# Requirements:
#   - python with `nuitka` installed
#   - a C compiler (gcc/clang/MSVC) available on PATH
#
# Behaviour in free-tier builds (public repo where premium/*.py does not
# exist): the globs match only __init__.py, the loops are no-ops, and the
# script exits 0. Downstream builds then produce a free-tier artifact.

set -euo pipefail

PYTHON="python"
for arg in "$@"; do
    case "$arg" in
        --uv) PYTHON="uv run python" ;;
    esac
done

PREMIUM_DIR="src/swingmusic/premium"

if [ ! -d "$PREMIUM_DIR" ]; then
    echo "error: $PREMIUM_DIR does not exist" >&2
    exit 1
fi

# Reset prior compilation artifacts before each run. cibuildwheel iterates
# over multiple Python versions against the same source tree; without this,
# .py sources deleted in iteration N would be missing in iteration N+1, and
# stale .so files from N would silently ship in N+1's wheel with the wrong
# ABI tag (cp311 .so inside a cp312 wheel, etc.).
if git rev-parse --git-dir >/dev/null 2>&1; then
    git checkout -- "$PREMIUM_DIR" 2>/dev/null || true
fi
find "$PREMIUM_DIR" -type f \( -name "*.so" -o -name "*.pyd" \) -delete

compile_file() {
    local py_path="$1"
    local target_dir
    target_dir="$(dirname "$py_path")"

    echo "nuitka --mode=module $py_path"
    $PYTHON -m nuitka \
        --mode=module \
        --nofollow-imports \
        --output-dir="$target_dir" \
        --remove-output \
        --no-pyi-file \
        --python-flag=no_docstrings \
        --python-flag=no_asserts \
        "$py_path"

    rm -f "$py_path"
}

# Top-level premium files (mixes.py, license.py, cloud.py, etc.)
shopt -s nullglob
for py in "$PREMIUM_DIR"/*.py; do
    [ "$(basename "$py")" = "__init__.py" ] && continue
    compile_file "$py"
done

# Nested premium/recipes/ files
for py in "$PREMIUM_DIR"/recipes/*.py; do
    [ "$(basename "$py")" = "__init__.py" ] && continue
    compile_file "$py"
done
shopt -u nullglob

# Verify produced .so files match the active interpreter's ABI tag. Catches
# the cibuildwheel matrix bug where stale .so from a prior iteration would
# slip into the next wheel undetected. Skipped in free-tier builds (no
# premium .py present, so no .so should have been produced).
expected_suffix=$($PYTHON -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
if [ -n "$expected_suffix" ]; then
    mismatched=$(find "$PREMIUM_DIR" -type f \( -name "*.so" -o -name "*.pyd" \) ! -name "*${expected_suffix}" 2>/dev/null || true)
    if [ -n "$mismatched" ]; then
        echo "error: compiled premium files do not match active Python's ABI suffix (${expected_suffix}):" >&2
        echo "$mismatched" >&2
        exit 1
    fi
fi

echo "premium module compilation complete"
