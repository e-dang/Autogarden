#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <factories/pin_factory.hpp>
#include <pins/logic_output_pinset.hpp>

TEST(LogicOutputPinSetTest, at) {
    const auto size = 5;
    PinMockFactory factory;
    auto tmpPins  = factory.createGenericPinVec<ILogicOutputPin, MockLogicOutputPin>(size);
    auto mockPins = factory.getMockPtrs<MockLogicOutputPin>(tmpPins);
    LogicOutputPinSet pinSet(std::move(tmpPins));

    for (int i = 0; i < size; i++) {
        EXPECT_EQ(pinSet.at(i), mockPins[i]);
    }
}
