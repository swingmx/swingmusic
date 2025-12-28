#!/bin/sh
set -e

if [ "$(id -u)" = "0" ]; then
    CURRENT_UID=$(id -u ${USER_NAME})
    CURRENT_GID=$(id -g ${USER_NAME})

    if [ "$PGID" != "$CURRENT_GID" ]; then
        groupmod -g "$PGID" ${USER_NAME}
    fi

    if [ "$PUID" != "$CURRENT_UID" ]; then
        usermod -u "$PUID" ${USER_NAME}
    fi

    chown -R ${USER_NAME}:${USER_NAME} /app /config 2>/dev/null || true

    exec gosu ${USER_NAME} "$@"
fi

exec "$@"
