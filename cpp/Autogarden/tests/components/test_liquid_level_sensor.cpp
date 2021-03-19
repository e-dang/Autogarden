#include <gtest/gtest.h>

#include <components/liquid_level_sensor/liquid_level_sensor.hpp>
#include <mocks/mock_arduino.hpp>
#include <mocks/mock_logic_input.hpp>
#include <suites/component_test_suite.hpp>

using namespace ::testing;
using ::testing::_;

class LiquidLevelSensorFactory {
public:
    std::unique_ptr<LiquidLevelSensor> create() {
        return std::make_unique<LiquidLevelSensor>(id, new MockLogicInputPin());
    }

    const String id = "testID";
};

INSTANTIATE_TYPED_TEST_SUITE_P(LiquidLevelSensor, ComponentTestSuite, LiquidLevelSensorFactory);

TEST(LiquidLevelSensorTest, read_returns_nullptr_if_input_pin_is_null) {
    LiquidLevelSensor sensor("id", nullptr, true);

    auto retVal = sensor.read();

    EXPECT_EQ(retVal, nullptr);
}

TEST(LiquidLevelSensorTest, read_returns_nullptr_if_process_signal_returns_false) {
    MockLogicInputPin* mockPin = new MockLogicInputPin();
    EXPECT_CALL(*mockPin, processSignal(_)).WillOnce(Return(false));
    LiquidLevelSensor sensor("id", mockPin, true);

    auto retVal = sensor.read();

    EXPECT_EQ(retVal, nullptr);
}

TEST(LiquidLevelSensorTest, read_returns_nullptr_if_propagateSignal_returns_false) {
    MockLogicInputPin* mockPin = new MockLogicInputPin();
    EXPECT_CALL(*mockPin, processSignal(_)).WillOnce(Return(true));
    LiquidLevelSensor sensor("id", mockPin, true);

    auto retVal = sensor.read();

    EXPECT_EQ(retVal, nullptr);
}