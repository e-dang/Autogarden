#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <component_test_suite.hpp>
#include <components/pump/pump.hpp>
#include <mock_logic_input.hpp>

using namespace ::testing;
using ::testing::_;

class PumpTest : public Test {
protected:
    std::string id = "pump";
    int onSig      = HIGH;
    int offSig     = LOW;
    NiceMock<MockLogicInputPin>* mockInputPin;
    std::unique_ptr<Pump> pump;

    void SetUp() {
        mockInputPin = new NiceMock<MockLogicInputPin>();
        pump         = std::make_unique<Pump>(id, mockInputPin, onSig, offSig);
    }
};

class PumpNullPinTest : public PumpTest {
protected:
    void SetUp() {
        mockInputPin = nullptr;
        PumpTest::SetUp();
    }
};

class PumpFactory {
public:
    std::unique_ptr<Pump> create() {
        return std::make_unique<Pump>(id, new MockLogicInputPin());
    }

    const std::string id = "testID";
};

INSTANTIATE_TYPED_TEST_SUITE_P(Pump, ComponentTestSuite, PumpFactory);

TEST_F(PumpTest, start_calls_processSignal_on_pin) {
    EXPECT_CALL(*mockInputPin, processSignal(_));

    pump->start();
}

TEST_F(PumpTest, pump_is_not_root_component) {
    EXPECT_FALSE(pump->isRoot());
}

TEST_F(PumpTest, stop_calls_processSignal_on_pin) {
    EXPECT_CALL(*mockInputPin, processSignal(_));

    pump->stop();
}

TEST_F(PumpNullPinTest, start_returns_false_with_null_pin) {
    EXPECT_FALSE(pump->start());
}

TEST_F(PumpNullPinTest, stop_returns_false_with_null_pin) {
    EXPECT_FALSE(pump->stop());
}