cmake_minimum_required(VERSION 3.16)
project(controku VERSION 0.0.1.20250717)

find_package(Qt6 REQUIRED COMPONENTS Widgets)
qt_standard_project_setup()
qt_add_executable(controku src/main.cpp)

find_package(PkgConfig REQUIRED)
pkg_check_modules(ROKUECP REQUIRED rokuecp)

target_link_libraries(controku PRIVATE ${ROKUECP_LIBRARIES} Qt6::Widgets)
target_include_directories(controku PRIVATE ${ROKUECP_INCLUDE_DIR})

set_target_properties(controku PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    WIN32_EXECUTABLE ON
    MACOSX_BUNDLE ON
)
