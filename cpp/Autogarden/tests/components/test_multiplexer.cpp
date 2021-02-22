#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/components.hpp>
#include <mocks/mock_logic_input.hpp>
#include <mocks/mock_logic_input_pinset.hpp>
#include <mocks/mock_logic_output_pinset.hpp>
#include <mocks/mock_translation_policy.hpp>
#include <suites/component_test_suite.hpp>

using namespace ::testing;
using ::testing::_;

class MultiplexerTest : public Test {
protected:
    const String id = "mux";
    MockLogicInputPinSet* inputPins;
    MockLogicOutputPinSet* outputPins;
    MockLogicInputPin* sigPin;
    MockLogicInputPin* enablePin;
    MockMultiplexerTranslationPolicy* policy;
    std::unique_ptr<Multiplexer> mux;

    MultiplexerTest() :
        inputPins(new MockLogicInputPinSet()),
        outputPins(new MockLogicOutputPinSet()),
        sigPin(new MockLogicInputPin()),
        enablePin(new MockLogicInputPin()),
        policy(new MockMultiplexerTranslationPolicy()),
        mux(new Multiplexer(id, inputPins, outputPins, sigPin, enablePin, policy)) {}
};

class MultiplexerFactory {
public:
    std::unique_ptr<Multiplexer> create() {
        return std::make_unique<Multiplexer>(id, new MockLogicInputPinSet(), new MockLogicOutputPinSet(),
                                             new MockLogicInputPin(), new MockLogicInputPin(),
                                             new MockMultiplexerTranslationPolicy());
    }

    const String id = "testID";
};

INSTANTIATE_TYPED_TEST_SUITE_P(Multiplexer, ComponentTestSuite, MultiplexerFactory);

TEST_F(MultiplexerTest, enable_returns_true_when_processSignal_returns_true) {
    EXPECT_CALL(*enablePin, processSignal(_)).WillRepeatedly(Return(true));

    EXPECT_TRUE(mux->enable());
    EXPECT_TRUE(mux->isEnabled());
    EXPECT_FALSE(mux->isDisabled());
}

TEST_F(MultiplexerTest, enable_returns_false_when_processSignal_returns_false) {
    EXPECT_CALL(*enablePin, processSignal(_)).WillRepeatedly(Return(false));
    auto prevState = mux->isDisabled();

    EXPECT_FALSE(mux->enable());
    EXPECT_EQ(mux->isEnabled(), !prevState);
    EXPECT_EQ(mux->isDisabled(), prevState);
}

TEST_F(MultiplexerTest, enable_returns_false_when_enablePin_is_nullptr) {
    Multiplexer mux(id, nullptr, nullptr, nullptr, nullptr, nullptr);
    auto prevState = mux.isDisabled();

    EXPECT_FALSE(mux.enable());
    EXPECT_EQ(mux.isEnabled(), !prevState);
    EXPECT_EQ(mux.isDisabled(), prevState);
}

TEST_F(MultiplexerTest, disable_returns_true_when_processSignal_returns_true) {
    EXPECT_CALL(*enablePin, processSignal(_)).WillRepeatedly(Return(true));
    auto prevState = mux->isDisabled();

    EXPECT_TRUE(mux->disable());
    EXPECT_FALSE(mux->isEnabled());
    EXPECT_TRUE(mux->isDisabled());
}

TEST_F(MultiplexerTest, disable_returns_false_when_processSignal_returns_false) {
    EXPECT_CALL(*enablePin, processSignal(_)).WillRepeatedly(Return(false));
    auto prevState = mux->isDisabled();

    EXPECT_FALSE(mux->disable());
    EXPECT_EQ(mux->isEnabled(), !prevState);
    EXPECT_EQ(mux->isDisabled(), prevState);
}

TEST_F(MultiplexerTest, disable_returns_false_when_enablePin_is_nullptr) {
    Multiplexer mux(id, nullptr, nullptr, nullptr, nullptr, nullptr);
    auto prevState = mux.isDisabled();

    EXPECT_FALSE(mux.disable());
    EXPECT_EQ(mux.isEnabled(), !prevState);
    EXPECT_EQ(mux.isDisabled(), prevState);
}

TEST_F(MultiplexerTest, mux_is_not_root_component) {
    EXPECT_FALSE(mux->isRoot());
}