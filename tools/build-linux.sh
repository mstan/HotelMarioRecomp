#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec python3 "$root/tools/build.py" --build-dir "${BUILD_DIR:-$root/build-linux}" --jobs "${BUILD_JOBS:-2}" "$@"
