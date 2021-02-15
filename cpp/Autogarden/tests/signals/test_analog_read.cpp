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
    PinMode mode     = PinMode::AnalogInput;
    NiceMock<MockTerminalPin> mockTerminalPin;
    NiceMock<MockArduino> mockArduino;
    AnalogRead signal;

    void SetUp() {
        ON_CALL(mockTerminalPin, getMode()).WillByDefault(Return(mode));
    }
};

class ParametrizedAnalogReadTest : public AnalogReadTest, public WithParamInterface<PinMode> {
protected:
    void SetUp() {
        mode = GetParam();
        AnalogReadTest::SetUp();
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

TEST_P(ParametrizedAnalogReadTest, execute_throw_runtime_error_if_pin_mode_is_not_analog_input) {
    try {
        signal.execute(&mockTerminalPin);
        FAIL() << "Expected std::runtime_error";
    } catch (std::runtime_error& error) {
        EXPECT_STREQ(error.what(), "Pinmode must be AnalogInput to write to this pin");
    } catch (...) {
        FAIL() << "Expected std::runtime_error";
    }
}

INSTANTIATE_TEST_SUITE_P(AnalogReadTest, ParametrizedAnalogReadTest,
                         Values(PinMode::DigitalOutput, PinMode::DigitalInput, PinMode::AnalogOutput));