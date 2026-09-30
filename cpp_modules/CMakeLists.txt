cmake_minimum_required(VERSION 3.28.3)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
project (
    myproject
    VERSION 1
    LANGUAGES CXX
)
add_compile_options(-Wall -Wpedantic -Werror -std=c++23)

include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY      https://github.com/google/googletest.git
  GIT_TAG main
)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG v2.13.6
)
FetchContent_MakeAvailable(googletest pybind11)

add_library(fast_diff
    fast_diff.cpp
    fast_diff.hpp
)
add_executable(fast_diff_tests
    fast_diff_tests.cpp
)
target_link_libraries(fast_diff_tests PRIVATE fast_diff GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(fast_diff_tests)

pybind11_add_module(fast_diff_extension
    bindings.cpp
)
target_link_libraries(fast_diff_extension PRIVATE fast_diff)
