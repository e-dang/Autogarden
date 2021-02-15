#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mock_arduino.hpp>
#include <mock_terminal.hpp>
#include <signals/analog_read.hpp>

using namespace ::testing;
using ::testing::_;

class AnalogReadTest : public Test {
protected:
    const int pinNum = 1;
    const int value  = 255;
    NiceMock<MockTerminalPin> mockTerminalPin;
    NiceMock<MockArduino> mockArduino;
    AnalogRead signal;

    AnalogReadTest() {
        ON_CALL(mockTerminalPin, getMode()).WillByDefault(Return(PinMode::AnalogInput));
    }
};

TEST_F(AnalogReadTest, execute_calls_analogRead_on_arduino_interface) {
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _analogRead(pinNum));
    EXPECT_CALL(mockTerminalPin, getPinNum()).WillRepeatedly(Return(pinNum));

    signal.execute(&mockTerminalPin);

    setMockArduino(nullptr);
}

TEST_F(AnalogReadTest, getValue_returns_the_return_value_from_analogRead) {
    setMockArduino(&mockArduino);
    ON_CALL(mockArduino, _analogRead(_)).WillByDefault(Return(value));

    signal.execute(&mockTerminalPin);

    setMockArduino(nullptr);

    EXPECT_EQ(signal.getValue(), value);
}