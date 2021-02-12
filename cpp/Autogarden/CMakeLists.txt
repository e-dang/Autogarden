cmake_minimum_required(VERSION 3.14)

project(Autogarden)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(GTest MODULE REQUIRED)

add_executable(test_autogarden tests/test_autogarden.cpp)

target_link_libraries(test_autogarden PRIVATE GTest::GTest)

gtest_discover_tests(test_autogarden)