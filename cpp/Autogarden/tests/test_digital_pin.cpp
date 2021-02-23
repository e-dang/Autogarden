#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <pins/digital_pin.hpp>

#include "mock_arduino.hpp"

using namespace ::testing;

class DigitalPinTest : public Test {
protected:
    uint8_t pinNum = 1;
    int value      = LOW;
    std::unique_ptr<DigitalPin> pin;

    DigitalPinTest() : pin(std::make_unique<DigitalPin>(pinNum, value)) {}
};

TEST_F(DigitalPinTest, getPin) {
    EXPECT_EQ(pin->getPin(), pinNum);
}

TEST_F(DigitalPinTest, isConnectedIsInitiallyFalse) {
    EXPECT_FALSE(pin->isConnected());
}

TEST_F(DigitalPinTest, isConnectedReturnsTrueAfterCallingsetIsConnectedWithTrue) {
    pin->setIsConnected(true);
    EXPECT_TRUE(pin->isConnected());
}

TEST_F(DigitalPinTest, getValue) {
    EXPECT_EQ(pin->getValue(), value);
}

TEST_F(DigitalPinTest, setValueSetsValueTo0IfLessThan0) {
    pin->setValue(-1);
    EXPECT_EQ(pin->getValue(), 0);
}

TEST_F(DigitalPinTest, setValueSetsValueTo0If0) {
    pin->setValue(0);
    EXPECT_EQ(pin->getValue(), 0);
}

TEST_F(DigitalPinTest, setValueSetsValueTo1If1) {
    pin->setValue(1);
    EXPECT_EQ(pin->getValue(), 1);
}

TEST_F(DigitalPinTest, setValueSetsValueTo1IfGreaterThan1) {
    pin->setValue(2);
    EXPECT_EQ(pin->getValue(), 1);
}

TEST_F(DigitalPinTest, getModeReturnsDigital) {
    EXPECT_EQ(pin->getMode(), PinMode::Digital);
}

TEST_F(DigitalPinTest, refreshCallsDigitalWrite) {
    MockArduino mockArduino;
    setMockArduino(&mockArduino);

    EXPECT_CALL(mockArduino, _digitalWrite(pinNum, value));

    pin->refresh();

    setMockArduino(nullptr);
}

TEST_F(DigitalPinTest, refreshAndSetValueToggleIsStale) {
    ASSERT_FALSE(pin->isStale());

    pin->setValue(0);

    ASSERT_TRUE(pin->isStale());

    pin->refresh();

    ASSERT_FALSE(pin->isStale());
}