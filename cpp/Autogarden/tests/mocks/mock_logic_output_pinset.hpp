#include <gmock/gmock.h>

#include <pins/interfaces/logic_output_pinset.hpp>

class MockLogicOutputPinSet : public ILogicOutputPinSet {
public:
    MOCK_METHOD(void, connect, (ILogicInputPinSet * inputPins), (override));
    MOCK_METHOD(void, connect, (ILogicInputPin * inputPin), (override));
    MOCK_METHOD(int, size, (), (const, override));
    MOCK_METHOD(ILogicOutputPin*, at, (const int& idx), (override));
};