#!/usr/bin/env bash

# Developer/admin tools installation

set -euo pipefail

log() {
    printf "\n==================================================\n"
    printf "%s\n" "$1"
    printf "==================================================\n"
}

export DEBIAN_FRONTEND=noninteractive

log "Installing Python tools"

apt-get update

apt-get install -y \
    python3 \
    python3-venv \
    python3-pip

# Virtuelle Python-Umgebung für den Lasttest
python3 -m venv /project/venv

# Python-Abhängigkeiten installieren
/project/venv/bin/python -m pip install --upgrade pip
/project/venv/bin/python -m pip install requests

# Lasttest-Skript ausführbar machen
chmod +x /project/influx_loadtest.py

log "Tools provisioning completed"