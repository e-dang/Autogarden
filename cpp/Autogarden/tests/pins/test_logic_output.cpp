#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <mock_signal.hpp>
#include <pins/logic_output.hpp>

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

TEST_P(ParametrizedLogicOutputPinTest, processSignal_saves_signal_to_instance_and_is_returned_by_popSignal) {
    MockSignal signal;

    EXPECT_TRUE(pin->processSignal(&signal));

    EXPECT_TRUE(pin->hasSignal());
    EXPECT_EQ(pin->popSignal(), &signal);
}

TEST_P(ParametrizedLogicOutputPinTest, hasSignal_is_initially_false) {
    EXPECT_FALSE(pin->hasSignal());
}

TEST_P(ParametrizedLogicOutputPinTest, popSignal_removes_signal_from_instance) {
    MockSignal signal;

    pin->processSignal(&signal);
    pin->popSignal();

    EXPECT_FALSE(pin->hasSignal());
}

TEST_P(ParametrizedLogicOutputPinTest, getMode_returns_mode) {
    EXPECT_EQ(pin->getMode(), mode);
}

TEST_F(LogicOutputPinTest, isConnected_is_initially_false) {
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(LogicOutputPinTest, connect_and_disconnect_toggle_isConnected) {
    pin->connect();
    EXPECT_TRUE(pin->isConnected());
    pin->disconnect();
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(LogicOutputPinTest, getPinNum_returns_pinNum) {
    EXPECT_EQ(pin->getPinNum(), pinNum);
}

TEST_F(LogicOutputPinTest, getSignalValue_returns_the_value_in_the_contained_signal) {
    const int value = HIGH;
    MockSignal signal;
    EXPECT_CALL(signal, getValue()).WillRepeatedly(Return(value));

    pin->processSignal(&signal);
    EXPECT_EQ(pin->getSignalValue(), value);
}

INSTANTIATE_TEST_SUITE_P(LogicOutputPinTest, ParametrizedLogicOutputPinTest,
                         Values(PinMode::DigitalOutput, PinMode::AnalogOutput, PinMode::DigitalInput,
                                PinMode::AnalogInput));