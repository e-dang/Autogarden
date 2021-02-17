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
    int pin8                       = 8;
    int pin9                       = 9;
    const std::string controllerId = "controller";
    MicroControllerFactory mcFactory;
    std::unique_ptr<MicroController> controller;

    const std::string valveId = "valve";
    const int valveOnSig      = HIGH;
    const int valveOffSig     = LOW;
    ValveFactory valveFactory;
    std::unique_ptr<IValve> valve;

    const std::string muxId = "mux";
    const int numMuxInputs  = 4;
    const int numMuxOutputs = 16;
    const PinMode muxMode   = PinMode::DigitalOutput;
    MultiplexerFactory muxFactory;
    std::unique_ptr<IMultiplexer> mux;

    NiceMock<MockArduino> mockArduino;

    ObjectWiringTest() {
        controller =
          mcFactory.create(controllerId, { pin0, pin1, pin2, pin3, pin4, pin5, pin6 }, {}, { pin7, pin8 }, { pin9 });
        valve = valveFactory.create(valveId, valveOnSig, valveOffSig);
        mux   = muxFactory.create(muxId, numMuxInputs, numMuxOutputs, muxMode);
    }
};

TEST_F(ObjectWiringTest, valve_attached_to_microcontroller) {
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, valveOnSig));
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, valveOffSig));

    ASSERT_TRUE(controller->appendChild(valve.get()));
    assertWiringIsCorrect(controller.get(), valve.get());

    ASSERT_TRUE(valve->open());
    ASSERT_TRUE(valve->close());

    setMockArduino(nullptr);
}

TEST_F(ObjectWiringTest, microcontroller_to_multiplexer_to_valve) {
    setMockArduino(&mockArduino);

    ASSERT_TRUE(controller->appendChild(mux.get()));
    assertWiringIsCorrect(controller.get(), mux.get());

    ASSERT_TRUE(mux->appendChild(valve.get()));
    assertWiringIsCorrect(mux.get(), valve.get());

    // mux transferring signal from valve
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, valveOnSig));
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, valveOffSig));

    // mux enable/disable
    EXPECT_CALL(mockArduino, _digitalWrite(pin1, HIGH)).Times(2);  // enabled
    EXPECT_CALL(mockArduino, _digitalWrite(pin1, LOW)).Times(2);   // disabled

    // mux logic inputs from open and close
    EXPECT_CALL(mockArduino, _digitalWrite(pin2, LOW)).Times(2);
    EXPECT_CALL(mockArduino, _digitalWrite(pin3, LOW)).Times(2);
    EXPECT_CALL(mockArduino, _digitalWrite(pin4, LOW)).Times(2);
    EXPECT_CALL(mockArduino, _digitalWrite(pin5, LOW)).Times(2);

    ASSERT_TRUE(valve->open());
    ASSERT_TRUE(valve->close());

    setMockArduino(nullptr);
}