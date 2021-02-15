#pragma once

#include <gmock/gmock.h>

#include <pins/interfaces/terminal.hpp>

class MockTerminalPin : public ITerminalPin {
public:
    MOCK_METHOD(void, initialize, (), (override));
    MOCK_METHOD(void, processSignal, (ISignal * signal), (override));
    MOCK_METHOD(int, getPinNum, (), (const, override));
    MOCK_METHOD(PinMode, getMode, (), (const, override));
    MOCK_METHOD(bool, isConnected, (), (const, override));
    MOCK_METHOD(void, connect, (), (override));
    MOCK_METHOD(void, disconnect, (), (override));
};