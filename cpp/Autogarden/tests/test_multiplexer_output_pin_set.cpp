#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/multiplexer/output_pin_set.hpp>

#include "mock_pin.hpp"

using namespace ::testing;

TEST(MultiplexerOutputPinSetTest, settingPinViewWillCauseAllOtherPinViewsToBeRefreshed) {
    const auto size   = 5;
    const auto mode   = PinMode::AnalogOutput;
    auto refreshValue = 0;
    auto value        = 1;
    std::vector<NiceMock<MockPin>> mockPins(size);
    std::vector<IPin*> vec;

    auto idx = 0;
    for (auto& mockPin : mockPins) {
        vec.push_back(&mockPin);
        ON_CALL(mockPin, getMode()).WillByDefault(Return(mode));
        if (idx != size - 1)
            EXPECT_CALL(mockPin, setValue(refreshValue));
        else
            EXPECT_CALL(mockPin, setValue(value));
        idx++;
    }

    MultiplexerOutputPinSet pinSet(std::move(vec));

    auto pinViews = pinSet.getNextAvailable(size, mode);
    pinViews.back().set(value);
}