#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mock_terminal.hpp>
#include <pins/terminal_pinset.hpp>

using namespace ::testing;

TEST(TerminalPinSetTest, at) {
    const auto size = 5;
    std::vector<MockTerminalPin*> mockPins(size);
    std::vector<std::unique_ptr<ITerminalPin>> pinPtrs;
    for (auto& mockPin : mockPins) {
        mockPin = new MockTerminalPin();
        pinPtrs.emplace_back(mockPin);
    }
    TerminalPinSet pinSet(std::move(pinPtrs));

    for (int i = 0; i < size; i++) {
        EXPECT_EQ(pinSet.at(i), mockPins[i]);
    }
}