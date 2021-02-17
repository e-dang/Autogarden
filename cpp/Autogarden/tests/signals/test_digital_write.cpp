#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mock_arduino.hpp>
#include <mock_terminal.hpp>
#include <signals/digital_write.hpp>

using namespace ::testing;

class DigitalWriteTest : public Test {
protected:
    const int pinNum = 1;
    const int value  = HIGH;
    PinMode mode     = PinMode::DigitalOutput;
    NiceMock<MockTerminalPin> mockTerminalPin;
    MockArduino mockArduino;
    DigitalWrite signal;

    DigitalWriteTest() : signal(value) {}

    void SetUp() {
        ON_CALL(mockTerminalPin, getMode()).WillByDefault(Return(mode));
    }
};

class ParametrizedDigitalWriteTest : public DigitalWriteTest, public WithParamInterface<PinMode> {
protected:
    void SetUp() {
        mode = GetParam();
        DigitalWriteTest::SetUp();
    }
};

TEST_F(DigitalWriteTest, execute_calls_digitalWrite_on_arduino_interface) {
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _digitalWrite(pinNum, value));
    EXPECT_CALL(mockTerminalPin, getPinNum()).WillRepeatedly(Return(pinNum));

    signal.execute(&mockTerminalPin);

    setMockArduino(nullptr);
}

TEST_F(DigitalWriteTest, getValue_returns_the_value_passed_into_the_constructor) {
    EXPECT_EQ(signal.getValue(), value);
}

TEST_P(ParametrizedDigitalWriteTest, execute_throw_runtime_error_if_pin_mode_is_not_digital_output) {
    try {
        signal.execute(&mockTerminalPin);
        FAIL() << "Expected std::runtime_error";
    } catch (std::runtime_error& error) {
        EXPECT_STREQ(error.what(), "Pinmode must be DigitalOutput to write to this pin");
    } catch (...) {
        FAIL() << "Expected std::runtime_error";
    }
}

INSTANTIATE_TEST_SUITE_P(DigitalWriteTest, ParametrizedDigitalWriteTest,
                         Values(PinMode::AnalogOutput, PinMode::DigitalInput, PinMode::AnalogInput));