cmake_minimum_required(VERSION 3.20)
project(HotelMarioRecomp C)

set(CDIRECOMP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../cdirecomp" CACHE PATH
    "Path to the sibling cdirecomp checkout")

if(NOT EXISTS "${CDIRECOMP_ROOT}/runner/CMakeLists.txt")
    message(FATAL_ERROR
        "cdirecomp was not found at ${CDIRECOMP_ROOT}. "
        "Clone it beside HotelMarioRecomp or set -DCDIRECOMP_ROOT=...")
endif()

set(CDI_COSIM_BUILD OFF CACHE BOOL "" FORCE)
set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
set(CDI_GAME_GENERATED_DIR "${CDIRECOMP_ROOT}/hotelmario/generated" CACHE PATH
    "Native modules generated from your Hotel Mario disc")
if(NOT EXISTS "${CDI_GAME_GENERATED_DIR}/module_manifest.c")
    message(FATAL_ERROR "Generate Hotel Mario native modules first: tools/build.ps1 -Disc <your.cue>")
endif()
if(NOT EXISTS "${CDIRECOMP_ROOT}/bios/generated/bios_identity.h")
    message(FATAL_ERROR "Regenerate the BIOS with the current CdiRecompBios to bind its byte identity")
endif()
add_subdirectory("${CDIRECOMP_ROOT}/runner"
                 "${CMAKE_BINARY_DIR}/cdirecomp-runtime")

set_target_properties(CdiRuntime PROPERTIES
    OUTPUT_NAME "HotelMarioRecomp"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
)
target_compile_definitions(CdiRuntime PRIVATE
    CDI_REQUIRE_DISC=1
    CDI_PRODUCT_NAME=\"HotelMarioRecomp\"
)
