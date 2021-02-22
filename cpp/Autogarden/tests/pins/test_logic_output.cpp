#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mocks/mock_signal.hpp>
#include <pins/logic_output.hpp>
#include <suites/pin_test_suite.hpp>

using namespace ::testing;

class LogicOutputPinTest : public Test {
protected:
    int pinNum   = 1;
    PinMode mode = PinMode::DigitalOutput;
    std::unique_ptr<LogicOutputPin> pin;

    void SetUp() {
        pin = std::make_unique<LogicOutputPin>(pinNum, mode);
    }
};

class ParametrizedLogicOutputPinTest : public LogicOutputPinTest, public WithParamInterface<PinMode> {
protected:
    void SetUp() {
        mode = GetParam();
        LogicOutputPinTest::SetUp();
    }
};

INSTANTIATE_TYPED_TEST_SUITE_P(LogicOutputPin, PinTestSuite, LogicOutputPin);

TEST_P(ParametrizedLogicOutputPinTest, processSignal_saves_signal_to_instance_and_is_returned_by_popSignal) {
    auto signal = std::make_shared<MockSignal>();

    EXPECT_TRUE(pin->processSignal(signal));

    EXPECT_TRUE(pin->hasSignal());
    EXPECT_EQ(pin->popSignal(), signal);
}

TEST_P(ParametrizedLogicOutputPinTest, hasSignal_is_initially_false) {
    EXPECT_FALSE(pin->hasSignal());
}

TEST_P(ParametrizedLogicOutputPinTest, popSignal_removes_signal_from_instance) {
    auto signal = std::make_shared<MockSignal>();

    pin->processSignal(signal);
    pin->popSignal();

    EXPECT_FALSE(pin->hasSignal());
}

TEST_F(LogicOutputPinTest, connect_and_disconnect_toggle_isConnected) {
    pin->connect();
    EXPECT_TRUE(pin->isConnected());
    pin->disconnect();
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(LogicOutputPinTest, getSignalValue_returns_the_value_in_the_contained_signal) {
    const int value = HIGH;
    auto signal     = std::make_shared<MockSignal>();
    EXPECT_CALL(*signal, getValue()).WillRepeatedly(Return(value));

    pin->processSignal(signal);
    EXPECT_EQ(pin->getSignalValue(), value);
}

INSTANTIATE_TEST_SUITE_P(LogicOutputPinTest, ParametrizedLogicOutputPinTest,
                         Values(PinMode::DigitalOutput, PinMode::AnalogOutput, PinMode::DigitalInput,
                                PinMode::AnalogInput));