#pragma once

#include <gmock/gmock.h>

#include <signals/interfaces/signal.hpp>

class MockSignal : public ISignal {
public:
    MOCK_METHOD(void, execute, (const ITerminalPin* pin), (override));
    MOCK_METHOD(int, getValue, (), (const, override));
};