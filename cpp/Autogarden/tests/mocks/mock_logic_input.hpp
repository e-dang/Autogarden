#pragma once

#include <gmock/gmock.h>

#include <pins/interfaces/logic_input.hpp>

class MockLogicInputPin : public ILogicInputPin {
public:
    MOCK_METHOD(bool, processSignal, (ISignal * signal), (override));
    MOCK_METHOD(int, getPinNum, (), (const, override));
    MOCK_METHOD(PinMode, getMode, (), (const, override));
    MOCK_METHOD(bool, connect, (IOutputPin * outputPin), (override));
};