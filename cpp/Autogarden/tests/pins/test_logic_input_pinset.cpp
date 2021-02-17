#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <mock_logic_input.hpp>
#include <mock_signal.hpp>
#include <pins/logic_input_pinset.hpp>

using namespace ::testing;

class LogicInputPinSetTest : public Test {
protected:
    int size = 5;
    std::vector<ILogicInputPin*> mockPins;
    std::vector<std::unique_ptr<ILogicInputPin>> tmpMockPins;
    std::unique_ptr<LogicInputPinSet> pinSet;

    void SetUp() {
        for (int i = 0; i < size; i++) {
            mockPins.push_back(new MockLogicInputPin());
            tmpMockPins.emplace_back(mockPins[i]);
        }
        pinSet = std::make_unique<LogicInputPinSet>(std::move(tmpMockPins));
    }
};

TEST_F(LogicInputPinSetTest, iterators_iterate_through_pins) {
    auto i = 0;
    for (auto& pin : *pinSet) {
        EXPECT_EQ(pin.get(), mockPins[i++]);
    }
}

TEST_F(LogicInputPinSetTest, at_returns_pin_at_idx) {
    EXPECT_EQ(pinSet->at(0), mockPins[0]);
}

TEST_F(LogicInputPinSetTest, size_returns_num_of_pins) {
    EXPECT_EQ(pinSet->size(), size);
}
