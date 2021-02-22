#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <mock_arduino.hpp>
#include <mock_signal.hpp>
#include <pin_test_suite.hpp>
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

class ParametrizedTerminalPinTest : public TerminalPinTest, public WithParamInterface<std::tuple<PinMode, int>> {
protected:
    void SetUp() {
        mode = std::get<0>(GetParam());
        TerminalPinTest::SetUp();
    }
};

INSTANTIATE_TYPED_TEST_SUITE_P(TerminalPin, PinTestSuite, TerminalPin);

TEST_P(ParametrizedTerminalPinTest, initialize_calls_pinMode_on_arduino_interface) {
    MockArduino mockArduino;
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _pinMode(pinNum, std::get<1>(GetParam())));

    pin->initialize();

    setMockArduino(nullptr);
}

TEST_F(TerminalPinTest, initialize_returns_false_when_unrecongized_pin_mode_is_used) {
    TerminalPin pin(pinNum, PinMode::Count);

    EXPECT_FALSE(pin.initialize());
}

TEST_P(ParametrizedTerminalPinTest, processSignal_calls_execute_on_signal_and_returns_true) {
    auto signal = std::make_shared<MockSignal>();
    EXPECT_CALL(*signal, execute(pin.get())).WillRepeatedly(Return(true));

    EXPECT_TRUE(pin->processSignal(signal));
}

TEST_F(TerminalPinTest, connect_and_disconnect_toggle_isConnected) {
    pin->connect();
    EXPECT_TRUE(pin->isConnected());
    pin->disconnect();
    EXPECT_FALSE(pin->isConnected());
}

INSTANTIATE_TEST_SUITE_P(TerminalPinTest, ParametrizedTerminalPinTest,
                         Values(std::tuple<PinMode, int>{ PinMode::DigitalOutput, OUTPUT },
                                std::tuple<PinMode, int>{ PinMode::AnalogOutput, OUTPUT },
                                std::tuple<PinMode, int>{ PinMode::DigitalInput, INPUT },
                                std::tuple<PinMode, int>{ PinMode::AnalogInput, INPUT }));