#pragma once

#include <gmock/gmock.h>

#include <components/multiplexer/oi_policy.hpp>

class MockOIPolicy : public IOutputToInputPolicy {
public:
    MOCK_METHOD(bool, execute, (IInputPinSet * inputPins, const IOutputPinSet* outputPins), (override));
};