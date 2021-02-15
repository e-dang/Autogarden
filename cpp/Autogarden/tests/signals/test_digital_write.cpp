#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mock_arduino.hpp>
#include <mock_terminal.hpp>
#include <signals/digital_write.hpp>

using namespace ::testing;

TEST(DigitalWrite, execute_calls_digitalWrite_on_arduino_interface) {
    const int pinNum = 1;
    const auto value = HIGH;
    NiceMock<MockTerminalPin> mockTerminalPin;
    MockArduino mockArduino;
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _digitalWrite(pinNum, value));
    EXPECT_CALL(mockTerminalPin, getPinNum()).WillRepeatedly(Return(pinNum));

    DigitalWrite signal(value);

    signal.execute(&mockTerminalPin);

    setMockArduino(nullptr);
}