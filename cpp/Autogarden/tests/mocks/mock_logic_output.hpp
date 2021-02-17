#pragma once

#include <gmock/gmock.h>

#include <pins/interfaces/logic_output.hpp>

class MockLogicOutputPin : public ILogicOutputPin {
public:
    MOCK_METHOD(bool, processSignal, (ISignal * signal), (override));
    MOCK_METHOD(int, getPinNum, (), (const, override));
    MOCK_METHOD(PinMode, getMode, (), (const, override));
    MOCK_METHOD(ISignal*, popSignal, (), (override));
    MOCK_METHOD(bool, hasSignal, (), (const, override));
    MOCK_METHOD(bool, isConnected, (), (const, override));
    MOCK_METHOD(void, connect, (), (override));
    MOCK_METHOD(void, disconnect, (), (override));
    MOCK_METHOD(int, getSignalValue, (), (const, override));
};