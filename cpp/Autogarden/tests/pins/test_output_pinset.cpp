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
    std::vector<std::unique_ptr<MockOutputPin>> tempMockPins;

    std::vector<MockLogicInputPin*> mockInputPins;
    std::vector<std::unique_ptr<ILogicInputPin>> tempMockInputPins;

    std::unique_ptr<LogicInputPinSet> inputPinSet;
    std::unique_ptr<OutputPinSet<std::unique_ptr<MockOutputPin>>> pinSet;

    void SetUp() {
        for (int i = 0; i < size; i++) {
            tempMockPins.emplace_back(new MockOutputPin());
            mockPins.push_back(tempMockPins[i].get());

            mockInputPins.emplace_back(new MockLogicInputPin());
            tempMockInputPins.emplace_back(mockInputPins[i]);
        }
        inputPinSet = std::make_unique<LogicInputPinSet>(std::move(tempMockInputPins));
        pinSet      = std::make_unique<OutputPinSet<std::unique_ptr<MockOutputPin>>>(std::move(tempMockPins));
    }
};

TEST_F(OutputPinSetTest, size_returns_num_pins) {
    EXPECT_EQ(pinSet->size(), size);
}

TEST_F(OutputPinSetTest, connect_calls_connect_on_each_input_pin_in_pin_set) {
    for (int i = 0; i < size; i++) {
        EXPECT_CALL(*mockInputPins[i], connect(mockPins[i])).WillRepeatedly(Return(true));
    }

    pinSet->connect(inputPinSet.get());
}

TEST_F(OutputPinSetTest, connect_calls_connect_on_input_pin) {
    const int idx  = 0;
    auto& inputPin = *mockInputPins[idx];
    EXPECT_CALL(inputPin, connect(mockPins[idx])).WillRepeatedly(Return(true));

    pinSet->connect(&inputPin);
}