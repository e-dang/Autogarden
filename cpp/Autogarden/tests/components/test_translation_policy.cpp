#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/components.hpp>
#include <mock_logic_input.hpp>
#include <mock_logic_input_pinset.hpp>
#include <mock_logic_output.hpp>
#include <mock_logic_output_pinset.hpp>
#include <mock_signal.hpp>
#include <mock_translation_policy.hpp>

using namespace ::testing;
using ::testing::_;

class MultiplexerTranslationPolicyTest : public Test {
protected:
    int numOutputPins = 2;
    int numInputPins  = 1;
    std::unique_ptr<NiceMock<MockLogicInputPinSet>> inputPins;
    std::unique_ptr<NiceMock<MockLogicOutputPinSet>> outputPins;
    std::unique_ptr<NiceMock<MockLogicOutputPin>> outputPin;
    std::unique_ptr<NiceMock<MockLogicInputPin>> inputPin;
    std::unique_ptr<NiceMock<MockLogicInputPin>> sigPin;
    std::shared_ptr<ISignal> signal;
    std::unique_ptr<MultiplexerTranslationPolicy> policy;

    MultiplexerTranslationPolicyTest() :
        inputPins(new NiceMock<MockLogicInputPinSet>()),
        outputPins(new NiceMock<MockLogicOutputPinSet>()),
        outputPin(new NiceMock<MockLogicOutputPin>()),
        inputPin(new NiceMock<MockLogicInputPin>()),
        sigPin(new NiceMock<MockLogicInputPin>()),
        signal(new NiceMock<MockSignal>()),
        policy(new MultiplexerTranslationPolicy()) {}
};

TEST_F(MultiplexerTranslationPolicyTest, translate_returns_true_and_sets_sig_pin_signal_to_instance_var) {
    ON_CALL(*outputPins, size()).WillByDefault(Return(numOutputPins));
    ON_CALL(*outputPins, at(_)).WillByDefault(Return(outputPin.get()));
    ON_CALL(*outputPin, hasSignal()).WillByDefault(Return(true));
    ON_CALL(*outputPin, popSignal()).WillByDefault(Return(signal));
    ON_CALL(*inputPins, size()).WillByDefault(Return(numInputPins));
    ON_CALL(*inputPins, at(_)).WillByDefault(Return(inputPin.get()));

    EXPECT_CALL(*inputPin, processSignal(_));

    EXPECT_TRUE(policy->translate(inputPins.get(), outputPins.get()));
    EXPECT_EQ(policy->getSigPinSignal(), signal);
}

TEST_F(MultiplexerTranslationPolicyTest, translate_returns_false) {
    ON_CALL(*outputPins, size()).WillByDefault(Return(numOutputPins));
    ON_CALL(*outputPins, at(_)).WillByDefault(Return(outputPin.get()));
    ON_CALL(*outputPin, hasSignal()).WillByDefault(Return(false));

    EXPECT_FALSE(policy->translate(inputPins.get(), outputPins.get()));
}