project(MyTiff C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

conan_basic_setup()

include_directories(${TIFF_INCLUDE_DIRS})
add_executable(tifftest tifftest.c)

target_link_libraries(tifftest ${CONAN_LIBS})
if(UNIX AND NOT APPLE)
    target_link_libraries(tifftest m)
endif()
