#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mock_arduino.hpp>
#include <mock_terminal.hpp>
#include <signals/analog_write.hpp>

using namespace ::testing;

class AnalogWriteTest : public Test {
protected:
    const int pinNum = 1;
    const int value  = 230;
    PinMode mode     = PinMode::AnalogOutput;
    NiceMock<MockTerminalPin> mockTerminalPin;
    MockArduino mockArduino;
    AnalogWrite signal;

    AnalogWriteTest() : signal(value) {}

    void SetUp() {
        ON_CALL(mockTerminalPin, getMode()).WillByDefault(Return(mode));
    }
};

class ParametrizedAnalogWriteTest : public AnalogWriteTest, public WithParamInterface<PinMode> {
protected:
    void SetUp() {
        mode = GetParam();
        AnalogWriteTest::SetUp();
    }
};

TEST_F(AnalogWriteTest, execute_calls_analogWrite_on_arduino_interface) {
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _analogWrite(pinNum, value));
    EXPECT_CALL(mockTerminalPin, getPinNum()).WillRepeatedly(Return(pinNum));

    signal.execute(&mockTerminalPin);

    setMockArduino(nullptr);
}

TEST_P(ParametrizedAnalogWriteTest, execute_throw_runtime_error_if_pin_mode_is_not_analog_output) {
    try {
        signal.execute(&mockTerminalPin);
        FAIL() << "Expected std::runtime_error";
    } catch (std::runtime_error& error) {
        EXPECT_STREQ(error.what(), "Pinmode must be AnalogOutput to write to this pin");
    } catch (...) {
        FAIL() << "Expected std::runtime_error";
    }
}

INSTANTIATE_TEST_SUITE_P(AnalogWriteTest, ParametrizedAnalogWriteTest,
                         Values(PinMode::DigitalOutput, PinMode::DigitalInput, PinMode::AnalogInput));