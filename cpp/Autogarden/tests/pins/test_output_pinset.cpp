#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <mock_logic_input.hpp>
#include <mock_output.hpp>
#include <pins/logic_input_pinset.hpp>
#include <pins/output_pinset.hpp>

using namespace ::testing;

class OutputPinSetTest : public Test {
protected:
    int size = 5;
    std::vector<MockOutputPin*> mockPins;
    std::vector<MockLogicInputPin> mockInputPins;
    std::vector<ILogicInputPin*> mockInputPinPtrs;
    std::unique_ptr<LogicInputPinSet> inputPinSet;
    std::unique_ptr<OutputPinSet<MockOutputPin*>> pinSet;

    OutputPinSetTest() : mockInputPins(size) {}

    void SetUp() {
        for (int i = 0; i < size; i++) {
            mockPins.push_back(new MockOutputPin());
            mockInputPinPtrs.push_back(&mockInputPins[i]);
        }
        inputPinSet = std::make_unique<LogicInputPinSet>(mockInputPinPtrs);
        pinSet      = std::make_unique<OutputPinSet<MockOutputPin*>>(mockPins);
    }

    ~OutputPinSetTest() {
        for (auto& pin : mockPins) {
            delete pin;
        }
    }
};

TEST_F(OutputPinSetTest, size_returns_num_pins) {
    EXPECT_EQ(pinSet->size(), size);
}

TEST_F(OutputPinSetTest, connect_calls_connect_on_each_input_pin_in_pin_set) {
    for (int i = 0; i < size; i++) {
        EXPECT_CALL(mockInputPins[i], connect(mockPins[i])).WillRepeatedly(Return(true));
    }

    pinSet->connect(inputPinSet.get());
}

TEST_F(OutputPinSetTest, connect_calls_connect_on_input_pin) {
    const int idx  = 0;
    auto& inputPin = mockInputPins[idx];
    EXPECT_CALL(inputPin, connect(mockPins[idx])).WillRepeatedly(Return(true));

    pinSet->connect(&inputPin);
}