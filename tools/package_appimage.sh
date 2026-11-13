#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec python3 "$root/tools/package.py" --build "${BUILD_DIR:-$root/build-linux}" "$@"
