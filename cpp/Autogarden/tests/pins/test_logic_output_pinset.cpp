#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <mock_logic_output.hpp>
#include <pins/logic_output_pinset.hpp>

using namespace ::testing;

TEST(LogicOutputPinSetTest, at) {
    const auto size = 5;
    std::vector<MockLogicOutputPin*> mockPins(size);
    std::vector<std::unique_ptr<ILogicOutputPin>> pinPtrs;
    for (auto& mockPin : mockPins) {
        mockPin = new MockLogicOutputPin();
        pinPtrs.emplace_back(mockPin);
    }
    LogicOutputPinSet pinSet(std::move(pinPtrs));

    for (int i = 0; i < size; i++) {
        EXPECT_EQ(pinSet.at(i), mockPins[i]);
    }
}
