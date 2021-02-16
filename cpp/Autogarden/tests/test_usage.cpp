#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/components.hpp>

#include "mock_arduino.hpp"

using namespace ::testing;

void assertWiringIsCorrect(Component* parent, Component* child) {
    ASSERT_TRUE(child->hasParent());
    ASSERT_EQ(parent->getChild(child->getId()), child);
    ASSERT_EQ(child->getParent(), parent);
}

class ObjectWiringTest : public Test {
protected:
    int pin0                       = 0;
    int pin1                       = 1;
    int pin2                       = 2;
    int pin3                       = 3;
    int pin4                       = 4;
    int pin5                       = 5;
    int pin6                       = 6;
    int pin7                       = 7;
    const std::string controllerId = "controller";
    const std::string valveId      = "valve";
    const int valveOnSig           = HIGH;
    const int valveOffSig          = LOW;

    MockArduino mockArduino;
    ValveFactory valveFactory;
    MicroControllerFactory mcFactory;
    std::unique_ptr<MicroController> controller;
    std::unique_ptr<IValve> valve;

    ObjectWiringTest() {
        controller = mcFactory.create(controllerId, { pin0, pin1, pin2, pin3 }, {}, { pin4, pin5 }, { pin6, pin7 });
        valve      = valveFactory.create(valveId, valveOnSig, valveOffSig);
    }
};

TEST_F(ObjectWiringTest, test_valve_attached_to_microcontroller) {
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, valveOnSig));
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, valveOffSig));

    controller->appendChild(valve.get());
    assertWiringIsCorrect(controller.get(), valve.get());
    valve->open();
    valve->close();

    setMockArduino(nullptr);
}
