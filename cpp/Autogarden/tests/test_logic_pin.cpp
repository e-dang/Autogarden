#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <pins/logic_pin.hpp>

using namespace ::testing;

class LogicPinTest : public Test {
protected:
    uint8_t pinNum = 1;
    int value      = 3;
    PinMode mode   = PinMode::Digital;

    std::unique_ptr<LogicPin> pin;

    LogicPinTest() : pin(std::make_unique<LogicPin>(pinNum, mode, value)) {}
};

class LogicPinParameterizedTest : public LogicPinTest, public WithParamInterface<PinMode> {};

TEST_F(LogicPinTest, getPin) {
    EXPECT_EQ(pin->getPin(), pinNum);
}

TEST_F(LogicPinTest, isConnectedIsInitiallyFalse) {
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(LogicPinTest, isConnectedReturnsTrueAfterCallingsetIsConnectedWithTrue) {
    pin->setIsConnected(true);
    EXPECT_TRUE(pin->isConnected());
}

TEST_F(LogicPinTest, getValue) {
    EXPECT_EQ(pin->getValue(), value);
}

TEST_F(LogicPinTest, setValueSetsValue) {
    pin->setValue(value + 1);
    EXPECT_EQ(pin->getValue(), value + 1);
}

TEST_F(LogicPinTest, getModeReturnsAnalogOutput) {
    EXPECT_EQ(pin->getMode(), mode);
}

TEST_P(LogicPinParameterizedTest, logicPinsCanBeAnyMode) {
    auto mode = GetParam();
    LogicPin pin(1, mode, 3);

    EXPECT_EQ(pin.getMode(), mode);
}

INSTANTIATE_TEST_SUITE_P(LogicPinTest, LogicPinParameterizedTest,
                         Values(PinMode::Digital, PinMode::AnalogInput, PinMode::AnalogOutput));