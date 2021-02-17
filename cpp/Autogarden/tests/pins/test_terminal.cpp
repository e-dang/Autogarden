#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <mock_arduino.hpp>
#include <mock_signal.hpp>
#include <pins/terminal.hpp>

using namespace ::testing;

class TerminalPinTest : public Test {
protected:
    int pinNum   = 1;
    PinMode mode = PinMode::DigitalOutput;
    std::unique_ptr<TerminalPin> pin;

    void SetUp() {
        pin = std::make_unique<TerminalPin>(pinNum, mode);
    }
};

class ParametrizedTerminalPinTest : public TerminalPinTest, public WithParamInterface<PinMode> {
protected:
    void SetUp() {
        mode = GetParam();
        TerminalPinTest::SetUp();
    }
};

TEST_P(ParametrizedTerminalPinTest, initialize_calls_pinMode_on_arduino_interface) {
    MockArduino mockArduino;
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _pinMode(pinNum, mode));

    pin->initialize();

    setMockArduino(nullptr);
}

TEST_F(TerminalPinTest, initialize_throws_runtime_error_when_pin_mode_count_is_used) {
    TerminalPin pin(pinNum, PinMode::Count);

    try {
        pin.initialize();
        FAIL() << "Expected std::runtime_error";
    } catch (std::runtime_error const& err) {
        EXPECT_STREQ(err.what(), "Pin mode not recongized - 4");
    } catch (...) {
        FAIL() << "Expected std::runtime_error";
    }
}

TEST_P(ParametrizedTerminalPinTest, processSignal_calls_execute_on_signal) {
    MockSignal signal;
    EXPECT_CALL(signal, execute(pin.get()));

    pin->processSignal(&signal);
}

TEST_P(ParametrizedTerminalPinTest, getMode_returns_mode) {
    EXPECT_EQ(pin->getMode(), mode);
}

TEST_F(TerminalPinTest, isConnected_is_initially_false) {
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(TerminalPinTest, connect_and_disconnect_toggle_isConnected) {
    pin->connect();
    EXPECT_TRUE(pin->isConnected());
    pin->disconnect();
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(TerminalPinTest, getPinNum_returns_pinNum) {
    EXPECT_EQ(pin->getPinNum(), pinNum);
}

INSTANTIATE_TEST_SUITE_P(TerminalPinTest, ParametrizedTerminalPinTest,
                         Values(PinMode::DigitalOutput, PinMode::AnalogOutput, PinMode::DigitalInput,
                                PinMode::AnalogInput));