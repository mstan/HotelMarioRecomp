#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
engine=${CDIRECOMP_ROOT:-"$root/../cdirecomp"}
build=${BUILD_DIR:-"$root/build-linux"}
modules=${CDI_GAME_GENERATED_DIR:-"$engine/hotelmario/generated"}
video=${CDI_VIDEO_BACKEND:-HLE}
loader=${CDI_LOADER_BACKEND:-HLE}
drawing=${CDI_DRAWING_BACKEND:-HLE}
memory=${CDI_MEMORY_BACKEND:-HLE}
service=${CDI_SERVICE_BACKEND:-HLE}
streaming=${CDI_STREAMING_BACKEND:-HLE}
board=${CDI_BOARD_BACKEND:-HLE}
jobs=${BUILD_JOBS:-4}
cmake -S "$root" -B "$build" -G Ninja -DCMAKE_BUILD_TYPE=Release \
    -DCDIRECOMP_ROOT="$engine" -DCDI_GAME_GENERATED_DIR="$modules" \
    -DCDI_VIDEO_BACKEND="$video" -DCDI_LOADER_BACKEND="$loader" \
    -DCDI_DRAWING_BACKEND="$drawing" -DCDI_MEMORY_BACKEND="$memory" \
    -DCDI_SERVICE_BACKEND="$service" -DCDI_STREAMING_BACKEND="$streaming" \
    -DCDI_BOARD_BACKEND="$board"
cmake --build "$build" --target CdiRuntime --parallel "$jobs"
