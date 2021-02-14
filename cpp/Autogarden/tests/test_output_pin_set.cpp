#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <pins/output_pin_set.hpp>

#include "mock_terminal_pin.hpp"

using namespace ::testing;

class OutputPinSetTest : public Test {
protected:
    int size = 3;
    std::vector<NiceMock<MockTerminalPin>> pinsOrig;
    std::vector<NiceMock<MockTerminalPin>*> pins;
    std::unique_ptr<OutputPinSet<NiceMock<MockTerminalPin>>> pinSet;

    OutputPinSetTest() : pinsOrig(size) {
        std::for_each(pinsOrig.begin(), pinsOrig.end(), [this](auto& pin) { this->pins.push_back(&pin); });
        pinSet = std::make_unique<OutputPinSet<NiceMock<MockTerminalPin>>>(std::move(pinsOrig));
    }
};

TEST_F(OutputPinSetTest, getNextAvailable) {
    const auto mode         = PinMode::Digital;
    const auto remaining    = 2;
    const auto numRequested = size - remaining;
    std::vector<uint8_t> expectedPinNums;
    expectedPinNums.reserve(numRequested);
    for (size_t i = 0; i < pins.size(); i++) {
        auto& pin = *pins[i];
        ON_CALL(pin, getPin()).WillByDefault(Return(i));
        ON_CALL(pin, getMode()).WillByDefault(Return(mode));
        if (i < remaining)
            ON_CALL(pin, isConnected()).WillByDefault(Return(true));
        else {
            ON_CALL(pin, isConnected()).WillByDefault(Return(false));
            expectedPinNums.push_back(static_cast<uint8_t>(i));
        }
    }

    auto pinViews = pinSet->getNextAvailable(numRequested, mode);
    std::vector<uint8_t> pinNums;
    std::transform(pinViews.begin(), pinViews.end(), std::back_inserter(pinNums),
                   [](const auto& view) { return view.getPin(); });
    ASSERT_THAT(pinNums, ContainerEq(expectedPinNums));
}

template <typename T>
int getNumAvailableSetUp(T& pins, const PinMode& mode) {
    auto count = 0;
    for (size_t i = 0; i < pins.size(); i++) {
        auto isOdd = static_cast<bool>(i % 2);
        auto& pin  = *pins[i];
        ON_CALL(pin, isConnected()).WillByDefault(Return(isOdd));
        ON_CALL(pin, getMode()).WillByDefault(Return(mode));
        if (!isOdd)
            count++;
    }

    return count;
}
TEST_F(OutputPinSetTest, getNumAvailable) {
    auto mode  = PinMode::Digital;
    auto count = getNumAvailableSetUp(pins, mode);

    EXPECT_EQ(pinSet->getNumAvailable(mode), count);
}

TEST_F(OutputPinSetTest, hasNumAvailableReturnsFalse) {
    auto mode         = PinMode::Digital;
    auto numAvailable = getNumAvailableSetUp(pins, mode);

    EXPECT_FALSE(pinSet->hasNumAvailable(numAvailable + 1, mode));
}

TEST_F(OutputPinSetTest, hasNumAvailableReturnsTrue) {
    auto mode         = PinMode::Digital;
    auto numAvailable = getNumAvailableSetUp(pins, mode);

    EXPECT_TRUE(pinSet->hasNumAvailable(numAvailable, mode));
}

TEST_F(OutputPinSetTest, getPinNumbers) {
    std::for_each(pins.begin(), pins.end(), [](auto& pin) { EXPECT_CALL(*pin, getPin()); });

    pinSet->getPinNumbers();
}

TEST_F(OutputPinSetTest, size) {
    ASSERT_EQ(pinSet->size(), size);
}

TEST_F(OutputPinSetTest, getPinValue) {
    const auto idx    = 0;
    const auto retVal = 1;
    auto& pin         = *pins[idx];
    ON_CALL(pin, getValue()).WillByDefault(Return(retVal));
    EXPECT_CALL(pin, getValue());

    EXPECT_EQ(pinSet->getPinValue(idx), retVal);
}

TEST_F(OutputPinSetTest, getPinValueThrowsIndexOutOfRange) {
    try {
        pinSet->getPinValue(pins.size());
        FAIL() << "Expected std::out_of_range";
    } catch (std::out_of_range const& err) {
        EXPECT_STREQ(err.what(), "vector");
    } catch (...) {
        FAIL() << "Expected std::out_of_range";
    }
}