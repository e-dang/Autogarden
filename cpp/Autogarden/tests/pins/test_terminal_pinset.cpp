#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <mock_terminal.hpp>
#include <pins/terminal_pinset.hpp>

using namespace ::testing;

TEST(TerminalPinSetTest, at) {
    const auto size = 5;
    std::vector<MockTerminalPin> mockPins(size);
    std::vector<ITerminalPin*> pinPtrs;
    for (auto& mockPin : mockPins) {
        pinPtrs.push_back(&mockPin);
    }
    TerminalPinSet pinSet(pinPtrs);

    for (int i = 0; i < size; i++) {
        EXPECT_EQ(pinSet.at(i), pinPtrs[i]);
    }
}