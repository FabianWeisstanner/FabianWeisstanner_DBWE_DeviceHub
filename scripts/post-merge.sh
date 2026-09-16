#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --disable-pip-version-check --no-input -r requirements.txt
python3 -m compileall -q app.py