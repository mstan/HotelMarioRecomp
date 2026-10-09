#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
engine=${CDIRECOMP_ROOT:-"$root/../cdirecomp"}
build=${BUILD_DIR:-"$root/build-linux"}
version=${VERSION:-0.0.2}
output=${OUTPUT:-"$root/dist/HotelMarioRecomp-v$version-linux-x86_64.AppImage"}
exec python3 "$engine/tools/package_runtime_appimage.py" \
    --product hotelmario --version "$version" \
    --runtime "$build/HotelMarioRecomp" \
    --apprun "$root/packaging/linux/AppRun" \
    --readme "$root/RUNTIME-README.md" \
    --config "$engine/player.cfg.example" \
    --notices "$engine/THIRD-PARTY-NOTICES.md" --out "$output"
