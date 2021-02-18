cmake_minimum_required(VERSION 3.14)

project(Autogarden)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_BUILD_TYPE Debug)
find_package(GTest REQUIRED CONFIG)

include_directories(include tests/mocks)

add_executable(test_autogarden  src/Arduino.cpp
                                tests/pins/test_terminal.cpp
                                tests/pins/test_logic_output.cpp
                                tests/pins/test_logic_input.cpp
                                tests/pins/test_logic_input_pinset.cpp
                                tests/pins/test_output_pinset.cpp
                                tests/pins/test_logic_output_pinset.cpp
                                tests/pins/test_terminal_pinset.cpp
                                tests/signals/test_digital_write.cpp
                                tests/signals/test_digital_read.cpp
                                tests/signals/test_analog_read.cpp
                                tests/signals/test_analog_write.cpp
                                tests/components/test_microcontroller.cpp
                                tests/components/test_valve.cpp
                                tests/components/test_multiplexer.cpp
                                tests/components/test_translation_policy.cpp
                                tests/test_usage.cpp
)

target_compile_definitions(test_autogarden PUBLIC LOW=0 HIGH=1 INPUT=0 OUTPUT=1 LSBFIRST=0 MSBFIRST=1)

target_link_libraries(test_autogarden PUBLIC GTest::gtest GTest::gmock GTest::gmock_main)