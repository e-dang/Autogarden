#include <gmock/gmock.h>

#include <pins/terminal_pin.hpp>

class MockTerminalPin : public ITerminalPin {
public:
    MOCK_METHOD(uint8_t, getPin, (), (const, override));
    MOCK_METHOD(bool, isConnected, (), (const, override));
    MOCK_METHOD(void, setIsConnected, (const bool& value), (override));
    MOCK_METHOD(int, getValue, (), (const, override));
    MOCK_METHOD(void, setValue, (const int& value), (override));
    MOCK_METHOD(PinMode, getMode, (), (const, override));
    MOCK_METHOD(bool, isStale, (), (const, override));
    MOCK_METHOD(void, refresh, (), (override));
    MOCK_METHOD(int, _scaleValue, (const int& value), (override));
};