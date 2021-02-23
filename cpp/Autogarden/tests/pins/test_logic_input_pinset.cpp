#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <factories/pin_factory.hpp>
#include <mocks/mock_signal.hpp>
#include <pins/logic_input_pinset.hpp>

using namespace ::testing;

class LogicInputPinSetTest : public Test {
protected:
    int size = 5;
    PinMockFactory factory;
    std::vector<MockLogicInputPin*> mockPins;
    std::vector<std::unique_ptr<ILogicInputPin>> tmpMockPins;
    std::unique_ptr<LogicInputPinSet> pinSet;

    void SetUp() {
        tmpMockPins = factory.createGenericPinVec<ILogicInputPin, MockLogicInputPin>(size);
        mockPins    = factory.getMockPtrs<MockLogicInputPin>(tmpMockPins);
        pinSet      = std::make_unique<LogicInputPinSet>(std::move(tmpMockPins));
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

TEST_F(LogicInputPinSetTest, disconnect_calls_disconnect_on_each_pin) {
    for (auto& pin : mockPins) {
        EXPECT_CALL(*pin, disconnect());
    }

    pinSet->disconnect();
}
