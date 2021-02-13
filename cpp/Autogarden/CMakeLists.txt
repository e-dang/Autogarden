cmake_minimum_required(VERSION 3.14)

project(Autogarden)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(GTest REQUIRED CONFIG)

include_directories(include)

add_executable(test_autogarden  tests/test_microcontroller.cpp
                                tests/test_digital_pin.cpp
                                tests/test_analog_output_pin.cpp
                                tests/test_analog_input_pin.cpp
                                tests/test_logic_pin.cpp
                                tests/test_terminal_pin_set.cpp
                                tests/test_usage.cpp
                                tests/test_output_pin_set.cpp
                                src/Arduino.cpp)

target_compile_definitions(test_autogarden PUBLIC LOW=0 HIGH=1)

target_link_libraries(test_autogarden PUBLIC GTest::gtest GTest::gmock GTest::gmock_main)