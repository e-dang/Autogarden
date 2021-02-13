#include <gmock/gmock.h>

#include <pins/terminal_pin_set.hpp>

template <typename T>
class MockTerminalPinSet : public ITerminalPinSet<T>
{
public:
    MOCK_METHOD(PinMode, getMode, (), (const, override));
    MOCK_METHOD(int, size, (), (const, override));
    MOCK_METHOD(std::vector<PinView>, getNextAvailable, (const int& requestedNum), (override));
    MOCK_METHOD(int, getNumAvailable, (), (const, override));
    MOCK_METHOD(std::vector<uint8_t>, getPinNumbers, (), (const, override));
    MOCK_METHOD(void, refresh, (), (override));
};