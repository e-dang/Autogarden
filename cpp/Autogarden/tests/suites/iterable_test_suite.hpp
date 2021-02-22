#pragma once

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <mock_terminal.hpp>
#include <pins/terminal_pinset.hpp>

using namespace ::testing;

template <typename T>
class PinSetTestSuite : public Test {
protected:
    const int size = 5;
    std::vector<MockTerminalPin*> mockPins;
    std::vector<std::unique_ptr<ITerminalPin>> pinPtrs;
    std::unique_ptr<T> pinSet;

    void SetUp() {
        for (int i = 0; i < size; i++) {
            mockPins.push_back(new MockTerminalPin());
            pinPtrs.emplace_back(mockPins[i]);
        }

        pinSet = std::make_unique<T>(std::move(pinPtrs));
    }
};

TYPED_TEST_SUITE_P(PinSetTestSuite);

TYPED_TEST_P(PinSetTestSuite, at) {
    for (int i = 0; i < this->size; i++) {
        EXPECT_EQ(this->pinSet->at(i), this->mockPins[i]);
    }
}

TYPED_TEST_P(PinSetTestSuite, iterator) {
    auto i = 0;
    for (auto& pin : *(this->pinSet)) {
        EXPECT_EQ(pin.get(), this->mockPins[i++]);
    }
}

REGISTER_TYPED_TEST_SUITE_P(PinSetTestSuite, at, iterator);