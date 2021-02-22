#pragma once

#include <gmock/gmock.h>

#include <pins/interfaces/terminal_pinset.hpp>

class MockTerminalPinSet : public ITerminalPinSet {
public:
    MOCK_METHOD(ITerminalPin*, at, (const int& idx), (override));
    MOCK_METHOD(bool, connect, (ILogicInputPinSet * inputPins), (override));
    MOCK_METHOD(bool, connect, (ILogicInputPin * inputPin), (override));
    MOCK_METHOD(int, size, (), (const, override));
    MOCK_METHOD(iterator, begin, (), (override));
    MOCK_METHOD(iterator, end, (), (override));
    MOCK_METHOD(void, merge, (std::unique_ptr<ITerminalPinSet> &&), (override));
};