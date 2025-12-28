#!/bin/sh
set -e

if [ "$(id -u)" = "0" ]; then
    CURRENT_UID=$(id -u ${USER_NAME})
    CURRENT_GID=$(id -g ${USER_NAME})

    if [ -n "${PGID:-}" ]; then
        case "$PGID" in
            *[!0-9]*)
                echo "Invalid PGID '$PGID': must be a non-empty numeric value." >&2
                exit 1
                ;;
        esac
        if [ "$PGID" != "$CURRENT_GID" ]; then
            groupmod -g "$PGID" ${USER_NAME}
        fi
    fi

    if [ -n "${PUID:-}" ]; then
        case "$PUID" in
            *[!0-9]*)
                echo "Invalid PUID '$PUID': must be a non-empty numeric value." >&2
                exit 1
                ;;
        esac
        if [ "$PUID" != "$CURRENT_UID" ]; then
            usermod -u "$PUID" ${USER_NAME}
        fi
    fi

    chown -R ${USER_NAME}:${USER_NAME} /app /config 2>/dev/null || true

    exec gosu ${USER_NAME} "$@"
fi

exec "$@"
