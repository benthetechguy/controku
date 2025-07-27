cmake_minimum_required(VERSION 3.16)
project(controku VERSION 2.0.0.20250717)

set(wxWidgets_CONFIGURATION mswu)
find_package(wxWidgets 3.2 COMPONENTS core base REQUIRED)
include(${wxWidgets_USE_FILE})
find_package(nlohmann_json 3.12 REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(ROKUECP REQUIRED rokuecp=0.2.0)

file(GLOB SOURCE "src/*.cpp")
add_executable(controku ${SOURCE})
target_link_libraries(controku PRIVATE ${wxWidgets_LIBRARIES} nlohmann_json::nlohmann_json ${ROKUECP_LIBRARIES})
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
