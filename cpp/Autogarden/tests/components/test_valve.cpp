#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/valve/valve.hpp>
#include <mock_logic_input.hpp>

using namespace ::testing;
using ::testing::_;

class ValveTest : public Test {
protected:
    std::string id = "valve";
    int onSig      = HIGH;
    int offSig     = LOW;
    NiceMock<MockLogicInputPin>* mockInputPin;
    std::unique_ptr<Valve> valve;

    void SetUp() {
        mockInputPin = new NiceMock<MockLogicInputPin>();
        valve        = std::make_unique<Valve>(id, mockInputPin, onSig, offSig);
    }
};

class ValveNullPinTest : public ValveTest {
protected:
    void SetUp() {
        mockInputPin = nullptr;
        ValveTest::SetUp();
    }
};

TEST_F(ValveTest, open_calls_processSignal_on_pin) {
    EXPECT_CALL(*mockInputPin, processSignal(_));

    valve->open();
}

TEST_F(ValveTest, close_calls_processSignal_on_pin) {
    EXPECT_CALL(*mockInputPin, processSignal(_));

    valve->close();
}

TEST_F(ValveNullPinTest, open_returns_false_with_null_pin) {
    EXPECT_FALSE(valve->open());
}

TEST_F(ValveNullPinTest, close_returns_false_with_null_pin) {
    EXPECT_FALSE(valve->close());
}