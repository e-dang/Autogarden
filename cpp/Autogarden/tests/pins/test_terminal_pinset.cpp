#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <iterable_test_suite.hpp>
#include <mock_terminal.hpp>
#include <pins/terminal_pinset.hpp>

using namespace ::testing;

INSTANTIATE_TYPED_TEST_SUITE_P(TerminalPinSet, PinSetTestSuite, TerminalPinSet);

TEST(TerminalPinSetTest, merge) {
    const auto size = 5;
    std::vector<MockTerminalPin*> mockPins1(size);
    std::vector<std::unique_ptr<ITerminalPin>> pinPtrs1;
    std::vector<MockTerminalPin*> mockPins2(size);
    std::vector<std::unique_ptr<ITerminalPin>> pinPtrs2;

    for (int i = 0; i < size; i++) {
        mockPins1.push_back(new MockTerminalPin());
        pinPtrs1.emplace_back(mockPins1[i]);

        mockPins2.push_back(new MockTerminalPin());
        pinPtrs2.emplace_back(mockPins2[i]);
    }
    std::unique_ptr<TerminalPinSet> pinSet1 = std::make_unique<TerminalPinSet>(std::move(pinPtrs1));
    std::unique_ptr<TerminalPinSet> pinSet2 = std::make_unique<TerminalPinSet>(std::move(pinPtrs2));

    pinSet1->merge(std::move(pinSet2));

    EXPECT_EQ(pinSet1->size(), size * 2);
    for (int i = 0; i < size; i++) {
        EXPECT_EQ(pinSet1->at(i), mockPins1[i]);
    }
    for (int i = size; i < size * 2; i++) {
        EXPECT_EQ(pinSet1->at(i), mockPins2[i - size]);
    }
}