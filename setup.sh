#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
git -C "$root" submodule update --init --recursive
exec python3 "$root/tools/build.py" "$@"
