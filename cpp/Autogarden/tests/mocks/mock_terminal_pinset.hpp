#pragma once

#include <gmock/gmock.h>

#include <pins/interfaces/terminal_pinset.hpp>

class MockTerminalPinSet : public ITerminalPinSet {
public:
    MOCK_METHOD(ITerminalPin*, at, (const int& idx), (override));
    MOCK_METHOD(void, connect, (ILogicInputPinSet * inputPins), (override));
    MOCK_METHOD(void, connect, (ILogicInputPin * inputPin), (override));
    MOCK_METHOD(int, size, (), (const, override));
};