#pragma once
#include <gmock/gmock.h>

#include <components/liquid_level_sensor/interfaces/liquid_level_sensor.hpp>

class MockLiquidLevelSensor : public ILiquidLevelSensor {
public:
    MOCK_METHOD(const char*, read, (), (override));
    MOCK_METHOD(bool, _setInputPins, (Component * parent), (override));
    MOCK_METHOD(IOutputPinSet*, _getOutputPins, (), (override));
};