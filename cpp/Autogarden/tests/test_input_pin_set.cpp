#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <pins/input_pin_set.hpp>

#include "mock_terminal_pin.hpp"

using namespace ::testing;

class InputPinSetTest : public Test {
protected:
    int size     = 3;
    PinMode mode = PinMode::Digital;
    std::vector<MockTerminalPin> mockPins;
    std::vector<PinView> pinViews;
    std::vector<PinView*> pinViewRefs;
    std::unique_ptr<InputPinSet> pinSet;

    InputPinSetTest() : mockPins(size) {
        for (int i = 0; i < size; i++) {
            pinViews.emplace_back(&mockPins[i]);
            pinViewRefs.push_back(&pinViews[i]);
        }
        pinSet = std::make_unique<InputPinSet>(std::move(pinViews), mode);
    }
};

class InputPinSetParametrizedTest : public InputPinSetTest, public WithParamInterface<int> {};

TEST_F(InputPinSetTest, getMode) {
    EXPECT_EQ(pinSet->getMode(), mode);
}

TEST_F(InputPinSetTest, size) {
    EXPECT_EQ(pinSet->size(), size);
}

TEST_P(InputPinSetParametrizedTest, connectToParentOutputReturnsFalseWhenParentOutputPinViewsIsIncorrectSize) {
    std::vector<MockTerminalPin> newMockPins(size + GetParam());
    std::vector<PinView> parentOutputPins;
    for (auto& mockPin : newMockPins) {
        parentOutputPins.emplace_back(&mockPin);
    }

    EXPECT_FALSE(pinSet->connectToOutput(std::move(parentOutputPins)));
}

INSTANTIATE_TEST_SUITE_P(InputPinSetTest, InputPinSetParametrizedTest, ::testing::Values(1, -1));

TEST_F(InputPinSetTest, setPin) {
    auto idx   = size - 1;
    auto value = 10;
    EXPECT_CALL(mockPins[idx], setValue(value));

    pinSet->setPin(idx, value);
}

TEST_F(InputPinSetTest, setPinUsesNewPinSetAfterConnectToParentOutputIsCalled) {
    std::vector<MockTerminalPin> newMockPins(size);
    std::vector<PinView> newPinViews;
    for (int i = 0; i < size; i++) {
        newPinViews.emplace_back(&newMockPins[i]);
    }
    auto* lastPinView = &newPinViews[size - 1];
    const auto idx    = size - 1;
    const auto value  = 12;

    EXPECT_CALL(newMockPins[size - 1], setValue(value));

    ASSERT_EQ(pinSet->connectToOutput(std::move(newPinViews)), true);
    pinSet->setPin(idx, value);
}

TEST_F(InputPinSetTest, setPinValueThrowsIndexOutOfRange) {
    try {
        pinSet->setPin(size, 1);
        FAIL() << "Expected std::out_of_range";
    } catch (std::out_of_range const& err) {
        EXPECT_STREQ(err.what(), "vector");
    } catch (...) {
        FAIL() << "Expected std::out_of_range";
    }
}