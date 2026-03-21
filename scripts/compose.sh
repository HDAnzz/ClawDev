#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

COMPOSE_FILES="-f docker-compose.yml"

if [ "$1" = "gpu" ]; then
    COMPOSE_FILES="$COMPOSE_FILES -f docker-compose.gpu.yml"
    shift
fi

case "$1" in
    exec)
        shift
        SERVICE="${1:-openclaw-gateway}"
        docker compose $COMPOSE_FILES exec "$SERVICE" "${@:-bash}"
        ;;
    logs)
        docker compose $COMPOSE_FILES logs -f openclaw-gateway
        ;;
    *)
        docker compose $COMPOSE_FILES "$@"
        ;;
esac
