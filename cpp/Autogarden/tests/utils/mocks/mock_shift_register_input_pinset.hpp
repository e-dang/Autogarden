#pragma once

#include <gmock/gmock.h>

#include <components/shift_register/interfaces/input_pinset.hpp>

class MockShiftRegisterInputPinSet : public IShiftRegisterInputPinSet {
public:
    MOCK_METHOD(bool, openLatch, (), (override));
    MOCK_METHOD(bool, closeLatch, (), (override));
    MOCK_METHOD(bool, shiftOut, (const int& binary), (override));
    MOCK_METHOD(iterator, begin, (), (override));
    MOCK_METHOD(iterator, end, (), (override));
    MOCK_METHOD(ILogicInputPin*, at, (const int& idx), (override));
    MOCK_METHOD(int, size, (), (const, override));
    MOCK_METHOD(void, disconnect, (), (override));
};
