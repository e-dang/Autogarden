#pragma once

#include <gmock/gmock.h>

#include <pins/output_pin_set.hpp>

class MockOutputPinSet : public IOutputPinSet {
public:
    MOCK_METHOD(std::vector<PinView>, getNextAvailable, (const int& requestedNum, const PinMode& pinMode), (override));
    MOCK_METHOD(int, getNumAvailable, (const PinMode& pinMode), (const, override));
    MOCK_METHOD(bool, hasNumAvailable, (const int& requestedNum, const PinMode& pinMode), (const, override));
    MOCK_METHOD(std::vector<uint8_t>, getPinNumbers, (), (const, override));
    MOCK_METHOD(int, getPinValue, (const int& idx), (const, override));
    MOCK_METHOD(int, size, (), (const, override));
    MOCK_METHOD(PinView, _createPinView, (IPin * pin), (override));
};