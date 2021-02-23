#include <gmock/gmock.h>

#include <pins/pin.hpp>

class MockPin : public IPin {
public:
    MOCK_METHOD(uint8_t, getPin, (), (const, override));
    MOCK_METHOD(bool, isConnected, (), (const, override));
    MOCK_METHOD(void, setIsConnected, (const bool& value), (override));
    MOCK_METHOD(int, getValue, (), (const, override));
    MOCK_METHOD(void, setValue, (const int& value), (override));
    MOCK_METHOD(PinMode, getMode, (), (const, override));
    MOCK_METHOD(int, _scaleValue, (const int& value), (override));
};