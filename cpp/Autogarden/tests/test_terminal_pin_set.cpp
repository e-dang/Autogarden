#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <pins/terminal_pin_set.hpp>

#include "mock_terminal_pin.hpp"

using namespace ::testing;

class TerminalPinSetTest : public Test
{
protected:
    int size = 3;
    std::vector<NiceMock<MockTerminalPin>> pinsOrig;
    std::vector<ITerminalPin*> pins;
    std::unique_ptr<TerminalPinSet> pinSet;

    TerminalPinSetTest() : pinsOrig(size)
    {
        std::for_each(pinsOrig.begin(), pinsOrig.end(), [this](auto& pin) { this->pins.push_back(&pin); });
        pinSet = std::make_unique<TerminalPinSet>(std::move(pins));
    }
};

TEST_F(TerminalPinSetTest, refresh)
{
    for (size_t i = 0; i < pins.size(); i++)
    {
        auto isOdd = static_cast<bool>(i % 2);
        auto& pin  = pinsOrig[i];
        ON_CALL(pin, isStale()).WillByDefault(Return(isOdd));
        if (isOdd)
            EXPECT_CALL(pin, refresh());
    }

    pinSet->refresh();
}