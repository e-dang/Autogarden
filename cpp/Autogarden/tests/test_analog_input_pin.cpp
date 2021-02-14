#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <pins/analog_input_pin.hpp>

#include "mock_arduino.hpp"

using namespace ::testing;

class AnalogInputPinTest : public Test {
protected:
    uint8_t pinNum = 1;
    int value      = 200;
    std::unique_ptr<AnalogInputPin> pin;

    AnalogInputPinTest() : pin(std::make_unique<AnalogInputPin>(pinNum, value)) {}
};

TEST_F(AnalogInputPinTest, getPin) {
    EXPECT_EQ(pin->getPin(), pinNum);
}

TEST_F(AnalogInputPinTest, isConnectedIsInitiallyFalse) {
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(AnalogInputPinTest, isConnectedReturnsTrueAfterCallingsetIsConnectedWithTrue) {
    pin->setIsConnected(true);
    EXPECT_TRUE(pin->isConnected());
}

TEST_F(AnalogInputPinTest, getValue) {
    EXPECT_EQ(pin->getValue(), value);
}

TEST_F(AnalogInputPinTest, setValueSetsValue) {
    auto value = 100;
    pin->setValue(value);
    EXPECT_EQ(pin->getValue(), value);
}

TEST_F(AnalogInputPinTest, getModeReturnsAnalogOutput) {
    EXPECT_EQ(pin->getMode(), PinMode::AnalogInput);
}

TEST_F(AnalogInputPinTest, refreshCallsAnalogWrite) {
    MockArduino mockArduino;
    setMockArduino(&mockArduino);

    EXPECT_CALL(mockArduino, _analogRead(pinNum));

    pin->refresh();

    setMockArduino(nullptr);
}

TEST_F(AnalogInputPinTest, refreshAndSetValueToggleIsStale) {
    ASSERT_FALSE(pin->isStale());

    pin->setValue(0);

    ASSERT_TRUE(pin->isStale());

    pin->refresh();

    ASSERT_FALSE(pin->isStale());
}