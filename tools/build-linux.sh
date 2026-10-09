#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
engine=${CDIRECOMP_ROOT:-"$root/../cdirecomp"}
build=${BUILD_DIR:-"$root/build-linux"}
modules=${CDI_GAME_GENERATED_DIR:-"$engine/hotelmario/generated"}
jobs=${BUILD_JOBS:-4}
cmake -S "$root" -B "$build" -G Ninja -DCMAKE_BUILD_TYPE=Release \
    -DCDIRECOMP_ROOT="$engine" -DCDI_GAME_GENERATED_DIR="$modules"
cmake --build "$build" --target CdiRuntime --parallel "$jobs"
