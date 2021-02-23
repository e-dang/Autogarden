#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mocks/mock_output.hpp>
#include <mocks/mock_signal.hpp>
#include <pins/logic_input.hpp>
#include <suites/pin_test_suite.hpp>

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

INSTANTIATE_TYPED_TEST_SUITE_P(LogicInput, PinTestSuite, LogicInputPin);

TEST_P(ParametrizedLogicInputPinTest,
       connect_saves_output_pin_to_instance_which_processSignal_then_calls_processSignal_on_with_signal) {
    std::shared_ptr<ISignal> mockSignal = std::make_shared<MockSignal>();
    NiceMock<MockOutputPin> mockOutputPin;
    EXPECT_CALL(mockOutputPin, isConnected()).WillRepeatedly(Return(false));
    EXPECT_CALL(mockOutputPin, getMode()).WillRepeatedly(Return(mode));
    EXPECT_CALL(mockOutputPin, processSignal(mockSignal)).WillRepeatedly(Return(true));

    EXPECT_TRUE(pin->connect(&mockOutputPin));
    ASSERT_EQ(pin->getOutputPin(), &mockOutputPin);
    EXPECT_TRUE(pin->processSignal(mockSignal));
    EXPECT_TRUE(pin->isConnected());
}

TEST_P(ParametrizedLogicInputPinTest, processSignal_returns_false_if_pin_has_not_been_connected) {
    std::shared_ptr<ISignal> mockSignal = std::make_shared<MockSignal>();
    ASSERT_EQ(pin->getOutputPin(), nullptr);
    EXPECT_FALSE(pin->processSignal(mockSignal));
}

TEST_F(LogicInputPinTest, connect_returns_false_when_output_pin_is_already_connected) {
    NiceMock<MockOutputPin> mockOutputPin;
    EXPECT_CALL(mockOutputPin, isConnected()).WillRepeatedly(Return(true));
    EXPECT_CALL(mockOutputPin, getMode()).WillRepeatedly(Return(mode));

    EXPECT_FALSE(pin->connect(&mockOutputPin));
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(LogicInputPinTest, connect_returns_false_when_output_pin_is_of_different_mode) {
    NiceMock<MockOutputPin> mockOutputPin;
    EXPECT_CALL(mockOutputPin, isConnected()).WillRepeatedly(Return(false));
    EXPECT_CALL(mockOutputPin, getMode()).WillRepeatedly(Return(static_cast<PinMode>((mode + 1) % 4)));

    EXPECT_FALSE(pin->connect(&mockOutputPin));
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(LogicInputPinTest, output_pin_is_initially_a_nullptr) {
    EXPECT_EQ(pin->getOutputPin(), nullptr);
}

INSTANTIATE_TEST_SUITE_P(LogicInputPinTest, ParametrizedLogicInputPinTest,
                         Values(PinMode::DigitalOutput, PinMode::AnalogOutput, PinMode::DigitalInput,
                                PinMode::AnalogInput));