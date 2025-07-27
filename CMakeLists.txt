cmake_minimum_required(VERSION 3.16)
project(controku VERSION 2.0.0.20250717)

set(wxWidgets_CONFIGURATION mswu)
find_package(wxWidgets COMPONENTS core base REQUIRED)
include(${wxWidgets_USE_FILE})

find_package(PkgConfig REQUIRED)
pkg_check_modules(ROKUECP REQUIRED rokuecp)

add_executable(controku src/main.cpp)
target_link_libraries(controku PRIVATE ${wxWidgets_LIBRARIES} ${ROKUECP_LIBRARIES})
target_include_directories(controku PRIVATE ${ROKUECP_INCLUDE_DIR})

configure_file(
    "src/version.h.in"
    "${CMAKE_CURRENT_BINARY_DIR}/version.h"
    @ONLY
)
target_include_directories(controku PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")

set_target_properties(controku PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)
