#pragma once

#include <gmock/gmock.h>

#include <pins/interfaces/output.hpp>

class MockOutputPin : public IOutputPin {
public:
    MOCK_METHOD(bool, processSignal, (std::shared_ptr<ISignal> signal), (override));
    MOCK_METHOD(int, getPinNum, (), (const, override));
    MOCK_METHOD(PinMode, getMode, (), (const, override));
    MOCK_METHOD(bool, isConnected, (), (const, override));
    MOCK_METHOD(void, connect, (), (override));
    MOCK_METHOD(void, disconnect, (), (override));
};