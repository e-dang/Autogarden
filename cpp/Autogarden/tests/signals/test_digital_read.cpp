#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mock_arduino.hpp>
#include <mock_terminal.hpp>
#include <signals/digital_read.hpp>

using namespace ::testing;
using ::testing::_;

class DigitalReadTest : public Test {
protected:
    const int pinNum = 1;
    const int value  = HIGH;
    NiceMock<MockTerminalPin> mockTerminalPin;
    MockArduino mockArduino;
    DigitalRead signal;

    DigitalReadTest() {
        ON_CALL(mockTerminalPin, getMode()).WillByDefault(Return(PinMode::DigitalInput));
    }
};

TEST_F(DigitalReadTest, execute_calls_digitalRead_on_arduino_interface) {
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _digitalRead(pinNum));
    EXPECT_CALL(mockTerminalPin, getPinNum()).WillRepeatedly(Return(pinNum));

    signal.execute(&mockTerminalPin);

    setMockArduino(nullptr);
}

TEST_F(DigitalReadTest, getValue_returns_the_return_value_from_digitalRead) {
    setMockArduino(&mockArduino);
    ON_CALL(mockArduino, _digitalRead(_)).WillByDefault(Return(value));

    signal.execute(&mockTerminalPin);

    setMockArduino(nullptr);

    EXPECT_EQ(signal.getValue(), value);
}