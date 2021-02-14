#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <pins/analog_output_pin.hpp>

#include "mock_arduino.hpp"

using namespace ::testing;

class AnalogOutputPinTest : public Test {
protected:
    uint8_t pinNum = 1;
    int value      = 200;
    std::unique_ptr<AnalogOutputPin> pin;

    AnalogOutputPinTest() : pin(std::make_unique<AnalogOutputPin>(pinNum, value)) {}
};

TEST_F(AnalogOutputPinTest, getPin) {
    EXPECT_EQ(pin->getPin(), pinNum);
}

TEST_F(AnalogOutputPinTest, isConnectedIsInitiallyFalse) {
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(AnalogOutputPinTest, isConnectedReturnsTrueAfterCallingsetIsConnectedWithTrue) {
    pin->setIsConnected(true);
    EXPECT_TRUE(pin->isConnected());
}

TEST_F(AnalogOutputPinTest, getValue) {
    EXPECT_EQ(pin->getValue(), value);
}

TEST_F(AnalogOutputPinTest, setValueSetsValueTo0IfLessThan0) {
    pin->setValue(-1);
    EXPECT_EQ(pin->getValue(), 0);
}

TEST_F(AnalogOutputPinTest, setValueSetsValueTo0If0) {
    pin->setValue(0);
    EXPECT_EQ(pin->getValue(), 0);
}

TEST_F(AnalogOutputPinTest, setValueSetsValueTo255If255) {
    pin->setValue(255);
    EXPECT_EQ(pin->getValue(), 255);
}

TEST_F(AnalogOutputPinTest, setValueSetsValueTo255IfGreaterThan256) {
    pin->setValue(256);
    EXPECT_EQ(pin->getValue(), 255);
}

TEST_F(AnalogOutputPinTest, getModeReturnsAnalogOutput) {
    EXPECT_EQ(pin->getMode(), PinMode::AnalogOutput);
}

TEST_F(AnalogOutputPinTest, refreshCallsAnalogWrite) {
    MockArduino mockArduino;
    setMockArduino(&mockArduino);

    EXPECT_CALL(mockArduino, _analogWrite(pinNum, value));

    pin->refresh();

    setMockArduino(nullptr);
}

TEST_F(AnalogOutputPinTest, refreshAndSetValueToggleIsStale) {
    ASSERT_FALSE(pin->isStale());

    pin->setValue(0);

    ASSERT_TRUE(pin->isStale());

    pin->refresh();

    ASSERT_FALSE(pin->isStale());
}