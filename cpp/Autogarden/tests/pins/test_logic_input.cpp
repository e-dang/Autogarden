#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <mock_output_pin.hpp>
#include <mock_signal.hpp>
#include <pins/logic_input.hpp>

using namespace ::testing;

class LogicInputPinTest : public Test {
protected:
    int pinNum   = 1;
    PinMode mode = PinMode::DigitalOutput;
    std::unique_ptr<LogicInputPin> pin;

    void SetUp() {
        pin = std::make_unique<LogicInputPin>(pinNum, mode);
    }
};

class ParametrizedLogicInputPinTest : public LogicInputPinTest, public WithParamInterface<PinMode> {
protected:
    void SetUp() {
        mode = GetParam();
        LogicInputPinTest::SetUp();
    }
};

TEST_P(ParametrizedLogicInputPinTest,
       connect_saves_output_pin_to_instance_which_processSignal_then_calls_processSignal_on_with_signal) {
    MockSignal mockSignal;
    NiceMock<MockOutputPin> mockOutputPin;
    EXPECT_CALL(mockOutputPin, isConnected()).WillRepeatedly(Return(false));
    EXPECT_CALL(mockOutputPin, getMode()).WillRepeatedly(Return(mode));
    EXPECT_CALL(mockOutputPin, processSignal(&mockSignal));

    EXPECT_TRUE(pin->connect(&mockOutputPin));
    pin->processSignal(&mockSignal);
}

TEST_F(LogicInputPinTest, connect_returns_false_when_output_pin_is_connected) {
    NiceMock<MockOutputPin> mockOutputPin;
    EXPECT_CALL(mockOutputPin, isConnected()).WillRepeatedly(Return(true));
    EXPECT_CALL(mockOutputPin, getMode()).WillRepeatedly(Return(mode));

    EXPECT_FALSE(pin->connect(&mockOutputPin));
}

TEST_F(LogicInputPinTest, connect_returns_false_when_output_pin_is_of_different_mode) {
    NiceMock<MockOutputPin> mockOutputPin;
    EXPECT_CALL(mockOutputPin, isConnected()).WillRepeatedly(Return(false));
    EXPECT_CALL(mockOutputPin, getMode()).WillRepeatedly(Return(static_cast<PinMode>((mode + 1) % 4)));

    EXPECT_FALSE(pin->connect(&mockOutputPin));
}

TEST_P(ParametrizedLogicInputPinTest, getMode_returns_mode) {
    EXPECT_EQ(pin->getMode(), mode);
}

TEST_F(LogicInputPinTest, getPinNum_returns_pinNum) {
    EXPECT_EQ(pin->getPinNum(), pinNum);
}

INSTANTIATE_TEST_SUITE_P(LogicInputPinTest, ParametrizedLogicInputPinTest,
                         Values(PinMode::DigitalOutput, PinMode::AnalogOutput, PinMode::DigitalInput,
                                PinMode::AnalogInput));