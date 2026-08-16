#!/usr/bin/env bash

set -euo pipefail

cd /project

# .env prüfen und laden
if [ ! -f .env ]; then
    echo "ERROR: /project/.env wurde nicht gefunden."
    exit 1
fi

set -a
source .env
set +a

# Python-venv automatisch erstellen, falls nicht vorhanden
if [ ! -x /project/venv/bin/python ]; then
    echo "==> Erstelle Python Virtual Environment..."

    python3 -m venv /project/venv

    echo "==> Installiere Python-Abhängigkeiten..."

    /project/venv/bin/python -m pip install --upgrade pip
    /project/venv/bin/python -m pip install requests
fi

echo "==> Starte InfluxDB Lasttest..."

exec /project/venv/bin/python \
    /project/influx_loadtest.py \
    "$@"