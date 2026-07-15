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
