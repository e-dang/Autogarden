#pragma once

#include <gmock/gmock.h>

#include <components/moisture_sensor/moisture_sensor.hpp>

class MockMoistureSensor : virtual public IMoistureSensor {
public:
    MOCK_METHOD(int, readRaw, (), (override));
    MOCK_METHOD(float, readScaled, (), (override));
    MOCK_METHOD(bool, _setInputPins, (Component * parent), (override));
    MOCK_METHOD(IOutputPinSet*, _getOutputPins, (), (override));
};