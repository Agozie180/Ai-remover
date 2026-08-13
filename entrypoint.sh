#!/bin/bash
set -e

if [ "$1" = "robust" ]; then
    shift
    exec python3 /app/robust_remover.py "$@"
elif [ "$1" = "basic" ] || [ "$1" = "remover" ]; then
    shift
    exec python3 /app/remover.py "$@"
else
    # Default to robust if first arg looks like a file
    exec python3 /app/robust_remover.py "$@"
fi
