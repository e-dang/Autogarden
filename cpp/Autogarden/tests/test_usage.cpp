#include <Arduino.h>
#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/components.hpp>

#include "mock_arduino.hpp"

using namespace ::testing;

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
    std::unique_ptr<IMicroController> controller;

    const std::string valveId = "valve";
    const int valveOnSig      = HIGH;
    const int valveOffSig     = LOW;
    ValveFactory valveFactory;
    std::vector<std::unique_ptr<IValve>> valves;

    const std::string dMuxId = "dMux";
    const int numDMuxInputs  = 4;
    const int numDMuxOutputs = 16;
    const PinMode dMuxMode   = PinMode::DigitalOutput;
    MultiplexerFactory muxFactory;
    std::unique_ptr<IMultiplexer> dMux;

    const std::string aMuxId = "aMux";
    const int numAMuxInputs  = 4;
    const int numAMuxOutputs = 16;
    const PinMode aMuxMode   = PinMode::AnalogInput;
    std::unique_ptr<IMultiplexer> aMux;

    const std::string regId = "reg";
    const int regNumOutputs = 8;
    const int regDirection  = MSBFIRST;
    ShiftRegisterFactory regFactory;
    std::unique_ptr<IShiftRegister> reg;

    const std::string sensorId = "sensor";
    const float sensorScaler   = 512. / 1023.;
    MoistureSensorFactory sensorFactory;
    std::vector<std::unique_ptr<IMoistureSensor>> sensors;

    NiceMock<MockArduino> mockArduino;

    ObjectWiringTest() {
        controller =
          mcFactory.create(controllerId, { pin0, pin1, pin2, pin3, pin4, pin5, pin6 }, {}, { pin7, pin8 }, { pin9 });
        dMux = muxFactory.create(dMuxId, numDMuxInputs, numDMuxOutputs, dMuxMode);
        aMux = muxFactory.create(aMuxId, numAMuxInputs, numAMuxOutputs, aMuxMode);
        reg  = regFactory.create(regId, regNumOutputs, regDirection);

        for (int i = 0; i < numDMuxOutputs; i++) {
            valves.emplace_back(valveFactory.create(valveId + std::to_string(i), valveOnSig, valveOffSig));
        }

        for (int i = 0; i < numAMuxOutputs; i++) {
            sensors.emplace_back(sensorFactory.create(sensorId + std::to_string(i), sensorScaler));
        }
    }
};

void assertWiringIsCorrect(Component* parent, Component* child) {
    ASSERT_TRUE(child->hasParent());
    ASSERT_EQ(parent->getChild(child->getId()), child);
    ASSERT_EQ(child->getParent(), parent);
    ASSERT_EQ(parent->getRoot(), child->getRoot());
}

TEST_F(ObjectWiringTest, valve_attached_to_microcontroller) {
    setMockArduino(&mockArduino);
    auto& valve = valves.back();

    EXPECT_CALL(mockArduino, _digitalWrite(pin0, valveOnSig));
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, valveOffSig));

    ASSERT_TRUE(controller->appendChild(valve.get()));
    assertWiringIsCorrect(controller.get(), valve.get());

    ASSERT_TRUE(valve->open());
    ASSERT_TRUE(valve->close());

    setMockArduino(nullptr);
}

TEST_F(ObjectWiringTest, moisture_sensor_to_microcontroller) {
    const int value = 456;
    auto& sensor    = sensors.back();
    setMockArduino(&mockArduino);
    EXPECT_CALL(mockArduino, _analogRead(pin9)).Times(2).WillRepeatedly(Return(value));

    ASSERT_TRUE(controller->appendChild(sensor.get()));
    assertWiringIsCorrect(controller.get(), sensor.get());

    EXPECT_EQ(sensor->readRaw(), value);
    EXPECT_FLOAT_EQ(sensor->readScaled(), static_cast<float>(value) * sensorScaler);

    setMockArduino(nullptr);
}

TEST_F(ObjectWiringTest, microcontroller_to_multiplexer_to_valve) {
    setMockArduino(&mockArduino);
    auto& valve = valves.back();

    ASSERT_TRUE(controller->appendChild(dMux.get()));
    assertWiringIsCorrect(controller.get(), dMux.get());

    ASSERT_TRUE(dMux->appendChild(valve.get()));
    assertWiringIsCorrect(dMux.get(), valve.get());

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

TEST_F(ObjectWiringTest, microcontroller_to_shift_register_to_multiplexer_to_valve) {
    setMockArduino(&mockArduino);
    auto& valve = valves.back();

    ASSERT_TRUE(controller->appendChild(reg.get()));
    assertWiringIsCorrect(controller.get(), reg.get());

    ASSERT_TRUE(reg->appendChild(dMux.get()));
    assertWiringIsCorrect(reg.get(), dMux.get());

    ASSERT_TRUE(dMux->appendChild(valve.get()));
    assertWiringIsCorrect(dMux.get(), valve.get());

    // valve on / off through mux sig pin
    EXPECT_CALL(mockArduino, _digitalWrite(pin3, valveOnSig));
    EXPECT_CALL(mockArduino, _digitalWrite(pin3, valveOffSig));

    // mux enable/disable
    EXPECT_CALL(mockArduino, _digitalWrite(pin4, HIGH)).Times(2);  // enabled
    EXPECT_CALL(mockArduino, _digitalWrite(pin4, LOW)).Times(2);   // disabled

    // shift register latch pin
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, LOW)).Times(2);
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, HIGH)).Times(2);

    // shift register shift out
    EXPECT_CALL(mockArduino, _shiftOut(pin1, pin2, regDirection, 0)).Times(2);

    ASSERT_TRUE(valve->open());
    ASSERT_TRUE(valve->close());

    setMockArduino(nullptr);
}

TEST_F(ObjectWiringTest, microcontroller_to_shift_register_to_two_multiplexers_to_valves_and_sensors) {
    const int value = 456;
    setMockArduino(&mockArduino);

    const auto numValves  = valves.size();
    const auto numSensors = sensors.size();

    ASSERT_TRUE(controller->appendChild(reg.get()));
    assertWiringIsCorrect(controller.get(), reg.get());

    ASSERT_TRUE(reg->appendChild(dMux.get()));
    assertWiringIsCorrect(reg.get(), dMux.get());

    ASSERT_TRUE(reg->appendChild(aMux.get()));
    assertWiringIsCorrect(reg.get(), aMux.get());

    for (auto& valve : valves) {
        ASSERT_TRUE(dMux->appendChild(valve.get()));
        assertWiringIsCorrect(dMux.get(), valve.get());
    }

    for (auto& sensor : sensors) {
        ASSERT_TRUE(aMux->appendChild(sensor.get()));
        assertWiringIsCorrect(aMux.get(), sensor.get());
    }

    // valve on / off through dMux sig pin
    EXPECT_CALL(mockArduino, _digitalWrite(pin3, valveOnSig)).Times(numValves);
    EXPECT_CALL(mockArduino, _digitalWrite(pin3, valveOffSig)).Times(numValves);

    // dMux enable/disable
    EXPECT_CALL(mockArduino, _digitalWrite(pin4, HIGH)).Times(numValves * 2);  // enabled
    EXPECT_CALL(mockArduino, _digitalWrite(pin4, LOW)).Times(numValves * 2);   // disabled

    // sensor readRaw and readScaled through aMux sig pin
    EXPECT_CALL(mockArduino, _analogRead(pin9)).Times(numSensors * 2).WillRepeatedly(Return(value));

    // aMux enable/disable
    EXPECT_CALL(mockArduino, _digitalWrite(pin5, HIGH)).Times(numSensors * 2);  // enabled
    EXPECT_CALL(mockArduino, _digitalWrite(pin5, LOW)).Times(numSensors * 2);   // disabled

    // shift register latch pin
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, LOW)).Times((numValves + numSensors) * 2);
    EXPECT_CALL(mockArduino, _digitalWrite(pin0, HIGH)).Times((numValves + numSensors) * 2);

    // shift register shift out for valve
    for (int i = 0; i < numValves - 1; i++) {
        EXPECT_CALL(mockArduino, _shiftOut(pin1, pin2, regDirection, i)).Times(2);
    }

    // overlap between valve and sensor calls
    EXPECT_CALL(mockArduino, _shiftOut(pin1, pin2, regDirection, numValves - 1)).Times(4);

    // shift register shift out for sensors
    for (int i = 1; i < numSensors; i++) {
        EXPECT_CALL(mockArduino, _shiftOut(pin1, pin2, regDirection, 15 | (i << 4))).Times(2);
    }

    for (auto& valve : valves) {
        EXPECT_TRUE(valve->open());
        EXPECT_TRUE(valve->close());
    }

    for (auto& sensor : sensors) {
        EXPECT_EQ(sensor->readRaw(), value);
        EXPECT_FLOAT_EQ(sensor->readScaled(), static_cast<float>(value) * sensorScaler);
    }

    setMockArduino(nullptr);
}