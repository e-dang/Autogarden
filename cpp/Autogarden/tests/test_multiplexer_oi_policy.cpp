#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/multiplexer/oi_policy.hpp>

#include "mock_input_pin_set.hpp"
#include "mock_output_pin_set.hpp"

using namespace ::testing;

TEST(MultiplexerOIPolicyTest, executeReturnsFalseWhenInputPinsIsNullPtr) {
    MultiplexerOIPolicy policy;
    MockOutputPinSet outputPinSet;

    EXPECT_FALSE(policy.execute(nullptr, &outputPinSet));
}

TEST(MultiplexerOIPolicyTest, executeReturnsFalseWhenOutputPinsIsNullPtr) {
    MultiplexerOIPolicy policy;
    MockInputPinSet inputPinSet;

    EXPECT_FALSE(policy.execute(&inputPinSet, nullptr));
}

TEST(MultiplexerOIPolicyTest, executeReturnsFalseWhenAllOutputsAreLow) {
    MultiplexerOIPolicy policy;
    MockInputPinSet inputPinSet;
    NiceMock<MockOutputPinSet> outputPinSet;
    const auto size = 5;

    ON_CALL(outputPinSet, size()).WillByDefault(Return(size));
    for (int i = 0; i < size; i++) {
        EXPECT_CALL(outputPinSet, getPinValue(i)).WillRepeatedly(Return(LOW));
    }

    EXPECT_FALSE(policy.execute(&inputPinSet, &outputPinSet));
}

TEST(MultiplexerOIPolicyTest, executeTranslatesOutputsToInputsAndReturnsTrue) {
    MultiplexerOIPolicy policy;
    NiceMock<MockInputPinSet> inputPinSet;
    NiceMock<MockOutputPinSet> outputPinSet;
    const auto size = 5;

    ON_CALL(outputPinSet, size()).WillByDefault(Return(size));
    ON_CALL(inputPinSet, size()).WillByDefault(Return(size));
    for (int i = 0; i < size; i++) {
        if (i < size - 1)
            EXPECT_CALL(outputPinSet, getPinValue(i)).WillRepeatedly(Return(LOW));
        else
            EXPECT_CALL(outputPinSet, getPinValue(size - 1)).WillRepeatedly(Return(HIGH));

        if (i == 2)
            EXPECT_CALL(inputPinSet, setPin(i, 1));
        else
            EXPECT_CALL(inputPinSet, setPin(i, 0));
    }

    EXPECT_TRUE(policy.execute(&inputPinSet, &outputPinSet));
}