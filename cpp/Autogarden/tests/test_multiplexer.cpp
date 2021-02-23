#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/multiplexer/multiplexer.hpp>
#include <memory>

#include "mock_input_pin_set.hpp"
#include "mock_oi_policy.hpp"
#include "mock_output_pin_set.hpp"

using namespace ::testing;

class MultiplexerTest : public Test {
protected:
    const std::string id     = "mux";
    const PinMode sigPinMode = PinMode::Digital;
    std::unique_ptr<MockInputPinSet> mockInputPins;
    std::unique_ptr<MockOutputPinSet> mockOutputPins;
    std::unique_ptr<MockOIPolicy> mockPolicy;
    std::unique_ptr<Multiplexer> mux;

    MultiplexerTest() :
        mux(
          std::make_unique<Multiplexer>(id, mockInputPins.get(), mockOutputPins.get(), mockPolicy.get(), sigPinMode)) {}
};

TEST_F(MultiplexerTest, getSigPinMode) {
    EXPECT_EQ(mux->getSigPinMode(), sigPinMode);
}

TEST_F(MultiplexerTest, enableReturnsFalseWhenInputsAreNotConnected) {
    EXPECT_FALSE(mux->enable());
}

TEST_F(MultiplexerTest, disableReturnsFalseWhenInputsAreNotConnected) {
    EXPECT_FALSE(mux->disable());
}