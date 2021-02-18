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
    PinMode mode     = PinMode::DigitalInput;
    NiceMock<MockTerminalPin> mockTerminalPin;
    NiceMock<MockArduino> mockArduino;
    DigitalRead signal;

    void SetUp() {
        ON_CALL(mockTerminalPin, getMode()).WillByDefault(Return(mode));
    }
};

class ParametrizedDigitalReadTest : public DigitalReadTest, public WithParamInterface<PinMode> {
protected:
    void SetUp() {
        mode = GetParam();
        DigitalReadTest::SetUp();
    }
};

TEST_F(DigitalReadTest, execute_calls_digitalRead_on_arduino_interface) {
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _digitalRead(pinNum));
    EXPECT_CALL(mockTerminalPin, getPinNum()).WillRepeatedly(Return(pinNum));

    EXPECT_TRUE(signal.execute(&mockTerminalPin));

    setMockArduino(nullptr);
}

TEST_F(DigitalReadTest, getValue_returns_the_return_value_from_digitalRead) {
    setMockArduino(&mockArduino);
    ON_CALL(mockArduino, _digitalRead(_)).WillByDefault(Return(value));

    signal.execute(&mockTerminalPin);

    setMockArduino(nullptr);

    EXPECT_EQ(signal.getValue(), value);
}

TEST_P(ParametrizedDigitalReadTest, execute_returns_false_if_pin_mode_is_not_digital_input) {
    EXPECT_FALSE(signal.execute(&mockTerminalPin));
}

INSTANTIATE_TEST_SUITE_P(DigitalReadTest, ParametrizedDigitalReadTest,
                         Values(PinMode::DigitalOutput, PinMode::AnalogOutput, PinMode::AnalogInput));