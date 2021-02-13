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
    std::vector<NiceMock<MockTerminalPin>*> pins;
    std::unique_ptr<TerminalPinSet<NiceMock<MockTerminalPin>>> pinSet;

    TerminalPinSetTest() : pinsOrig(size), pins()
    {
        std::for_each(pinsOrig.begin(), pinsOrig.end(), [this](auto& pin) { this->pins.push_back(&pin); });
        pinSet = std::make_unique<TerminalPinSet<NiceMock<MockTerminalPin>>>(std::move(pinsOrig));
    }
};

TEST_F(TerminalPinSetTest, refresh)
{
    for (size_t i = 0; i < pins.size(); i++)
    {
        auto isOdd = static_cast<bool>(i % 2);
        auto& pin  = *pins[i];
        ON_CALL(pin, isStale()).WillByDefault(Return(isOdd));
        if (isOdd)
            EXPECT_CALL(pin, refresh());
    }

    pinSet->refresh();
}