#pragma once

#include <gmock/gmock.h>

#include <components/microcontroller/interfaces/microcontroller.hpp>

class MockMicroController : public IMicroController {
public:
    MOCK_METHOD(bool, initialize, (), (override));
    MOCK_METHOD(bool, _setInputPins, (Component * parent), (override));
    MOCK_METHOD(IOutputPinSet*, _getOutputPins, (), (override));
};