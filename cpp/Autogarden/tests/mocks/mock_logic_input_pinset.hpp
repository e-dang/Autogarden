#pragma once

#include <gmock/gmock.h>

#include <pins/interfaces/logic_input_pinset.hpp>

class MockLogicInputPinSet : public ILogicInputPinSet {
public:
    MOCK_METHOD(iterator, begin, (), (override));
    MOCK_METHOD(iterator, end, (), (override));
    MOCK_METHOD(ILogicInputPin*, at, (const int& idx), (override));
    MOCK_METHOD(int, size, (), (const, override));
};