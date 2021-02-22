#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <factories/pin_factory.hpp>
#include <pins/terminal_pinset.hpp>
#include <suites/iterable_test_suite.hpp>

INSTANTIATE_TYPED_TEST_SUITE_P(TerminalPinSet, PinSetTestSuite, TerminalPinSet);

TEST(TerminalPinSetTest, merge) {
    const auto size = 5;
    PinMockFactory factory;
    auto tmpPins1  = factory.createGenericPinVec<ITerminalPin, MockTerminalPin>(size);
    auto mockPins1 = factory.getMockPtrs<MockTerminalPin>(tmpPins1);
    auto tmpPins2  = factory.createGenericPinVec<ITerminalPin, MockTerminalPin>(size);
    auto mockPins2 = factory.getMockPtrs<MockTerminalPin>(tmpPins2);

    std::unique_ptr<TerminalPinSet> pinSet1 = std::make_unique<TerminalPinSet>(std::move(tmpPins1));
    std::unique_ptr<TerminalPinSet> pinSet2 = std::make_unique<TerminalPinSet>(std::move(tmpPins2));

    pinSet1->merge(std::move(pinSet2));

    EXPECT_EQ(pinSet1->size(), size * 2);
    for (int i = 0; i < size; i++) {
        EXPECT_EQ(pinSet1->at(i), mockPins1[i]);
    }
    for (int i = size; i < size * 2; i++) {
        EXPECT_EQ(pinSet1->at(i), mockPins2[i - size]);
    }
}