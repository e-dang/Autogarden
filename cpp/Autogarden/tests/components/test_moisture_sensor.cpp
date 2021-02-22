#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <component_test_suite.hpp>
#include <components/components.hpp>
#include <mock_arduino.hpp>
#include <mock_logic_input.hpp>
#include <mock_signal.hpp>
#include <mock_terminal.hpp>

using namespace ::testing;
using ::testing::_;

class MoistureSensorTest : public Test {
protected:
    const String id = "sensor";
    MockLogicInputPin* mockInputPin;
    const float scaler    = .782;
    const int errorSignal = INT32_MIN;
    std::unique_ptr<MoistureSensor> sensor;

    MoistureSensorTest() {
        mockInputPin = new MockLogicInputPin();
        sensor       = std::make_unique<MoistureSensor>(id, mockInputPin, scaler);
    }

    void useNullInputPin() {
        sensor = std::make_unique<MoistureSensor>(id, nullptr, scaler);
    }
};

class MoistureSensorFactory {
public:
    std::unique_ptr<MoistureSensor> create() {
        return std::make_unique<MoistureSensor>(id, new MockLogicInputPin());
    }

    const String id = "testID";
};

INSTANTIATE_TYPED_TEST_SUITE_P(MoistureSensor, ComponentTestSuite, MoistureSensorFactory);

TEST_F(MoistureSensorTest, readRaw_returns_error_num_if_input_pin_is_null) {
    useNullInputPin();

    EXPECT_EQ(sensor->readRaw(), errorSignal);
}

TEST_F(MoistureSensorTest, readRaw_returns_error_num_if_process_signal_returns_false) {
    EXPECT_CALL(*mockInputPin, processSignal(_)).WillOnce(Return(false));

    EXPECT_EQ(sensor->readRaw(), errorSignal);
}

TEST_F(MoistureSensorTest, readRaw_returns_error_num_if_propagateSignal_returns_false) {
    EXPECT_CALL(*mockInputPin, processSignal(_)).WillOnce(Return(true));

    EXPECT_EQ(sensor->readRaw(), errorSignal);
}

TEST_F(MoistureSensorTest, readScaled_returns_error_num_if_input_pin_is_null) {
    useNullInputPin();

    EXPECT_FLOAT_EQ(sensor->readScaled(), static_cast<float>(errorSignal));
}

TEST_F(MoistureSensorTest, readScaled_returns_error_num_if_process_signal_returns_false) {
    EXPECT_CALL(*mockInputPin, processSignal(_)).WillOnce(Return(false));

    EXPECT_FLOAT_EQ(sensor->readScaled(), static_cast<float>(errorSignal));
}

TEST_F(MoistureSensorTest, readScaled_returns_error_num_if_propagateSignal_returns_false) {
    EXPECT_CALL(*mockInputPin, processSignal(_)).WillOnce(Return(true));

    EXPECT_FLOAT_EQ(sensor->readRaw(), static_cast<float>(errorSignal));
}