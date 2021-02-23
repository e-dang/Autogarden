#pragma once

#include <gmock/gmock.h>

#include <pins/input_pin_set.hpp>

class MockInputPinSet : public IInputPinSet {
public:
    MOCK_METHOD(bool, connectToOutput, (std::vector<PinView> && outputPins), (override));
    MOCK_METHOD(void, setPin, (const int& idx, const int& value), (override));
    MOCK_METHOD(PinMode, getMode, (), (const, override));
    MOCK_METHOD(int, size, (), (const, override));
};