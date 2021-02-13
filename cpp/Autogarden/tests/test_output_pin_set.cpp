#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <pins/output_pin_set.hpp>

#include "mock_terminal_pin.hpp"

using namespace ::testing;

class GenericOutputPinSetTest : public Test
{
protected:
    int size = 3;
    std::vector<NiceMock<MockTerminalPin>> pinsOrig;
    std::vector<NiceMock<MockTerminalPin>*> pins;
    std::unique_ptr<GenericOutputPinSet<NiceMock<MockTerminalPin>>> pinSet;

    GenericOutputPinSetTest() : pinsOrig(size)
    {
        std::for_each(pinsOrig.begin(), pinsOrig.end(), [this](auto& pin) { this->pins.push_back(&pin); });
        pinSet = std::make_unique<GenericOutputPinSet<NiceMock<MockTerminalPin>>>(std::move(pinsOrig));
    }
};

TEST_F(GenericOutputPinSetTest, getNextAvailable)
{
    const auto remaining    = 2;
    const auto numRequested = size - remaining;
    std::vector<uint8_t> expectedPinNums;
    expectedPinNums.reserve(numRequested);
    for (size_t i = 0; i < pins.size(); i++)
    {
        auto& pin = *pins[i];
        ON_CALL(pin, getPin()).WillByDefault(Return(i));
        if (i < remaining)
            ON_CALL(pin, isConnected()).WillByDefault(Return(true));
        else
        {
            ON_CALL(pin, isConnected()).WillByDefault(Return(false));
            expectedPinNums.push_back(static_cast<uint8_t>(i));
        }
    }

    auto pinViews = pinSet->getNextAvailable(numRequested);
    std::vector<uint8_t> pinNums;
    std::transform(pinViews.begin(), pinViews.end(), std::back_inserter(pinNums),
                   [](const auto& view) { return view.getPin(); });
    ASSERT_THAT(pinNums, ContainerEq(expectedPinNums));
}

TEST_F(GenericOutputPinSetTest, getNumAvailable)
{
    auto count = 0;
    for (size_t i = 0; i < pins.size(); i++)
    {
        auto isOdd = static_cast<bool>(i % 2);
        auto& pin  = *pins[i];
        ON_CALL(pin, isConnected()).WillByDefault(Return(isOdd));
        if (!isOdd)
            count++;
    }

    EXPECT_EQ(pinSet->getNumAvailable(), count);
}

TEST_F(GenericOutputPinSetTest, getPinNumbers)
{
    std::for_each(pins.begin(), pins.end(), [](auto& pin) { EXPECT_CALL(*pin, getPin()); });

    pinSet->getPinNumbers();
}

TEST_F(GenericOutputPinSetTest, getMode)
{
    auto mode = PinMode::Digital;

    ON_CALL(*pins[0], getMode()).WillByDefault(Return(mode));
    EXPECT_CALL(*pins[0], getMode());

    EXPECT_EQ(pinSet->getMode(), mode);
}

TEST_F(GenericOutputPinSetTest, size) { ASSERT_EQ(pinSet->size(), size); }
