#!/bin/bash
set -euo pipefail

OUT_DIR="src/python-helpers"
mkdir -p "$OUT_DIR"

uv export -o "$OUT_DIR/pylock.toml"
uv pip freeze > "$OUT_DIR/requirements.txt"

echo "✔️ Updated lockfiles in $OUT_DIR"
