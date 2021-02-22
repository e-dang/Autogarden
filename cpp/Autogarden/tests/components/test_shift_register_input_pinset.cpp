#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/components.hpp>
#include <mocks/mock_arduino.hpp>
#include <mocks/mock_logic_input.hpp>
#include <mocks/mock_output.hpp>

using namespace ::testing;
using ::testing::_;

class ShiftRegisterInputPinSetTest : public Test {
protected:
    const int direction   = LSBFIRST;
    const int latchPinNum = 0;
    const int dataPinNum  = 1;
    const int clockPinNum = 2;

    NiceMock<MockOutputPin> mockLatchOutputPin;
    NiceMock<MockOutputPin> mockDataOutputPin;
    NiceMock<MockOutputPin> mockClockOutputPin;

    NiceMock<MockLogicInputPin>* mockLatchPin;
    NiceMock<MockLogicInputPin>* mockDataPin;
    NiceMock<MockLogicInputPin>* mockClockPin;
    std::unique_ptr<ShiftRegisterInputPinSet> inputPinSet;

    ShiftRegisterInputPinSetTest() {
        ON_CALL(mockLatchOutputPin, getPinNum()).WillByDefault(Return(latchPinNum));
        ON_CALL(mockDataOutputPin, getPinNum()).WillByDefault(Return(dataPinNum));
        ON_CALL(mockClockOutputPin, getPinNum()).WillByDefault(Return(clockPinNum));

        mockLatchPin = new NiceMock<MockLogicInputPin>();
        mockDataPin  = new NiceMock<MockLogicInputPin>();
        mockClockPin = new NiceMock<MockLogicInputPin>();

        ON_CALL(*mockLatchPin, getOutputPin()).WillByDefault(Return(&mockLatchOutputPin));
        ON_CALL(*mockDataPin, getOutputPin()).WillByDefault(Return(&mockDataOutputPin));
        ON_CALL(*mockClockPin, getOutputPin()).WillByDefault(Return(&mockClockOutputPin));
        inputPinSet = std::make_unique<ShiftRegisterInputPinSet>(mockLatchPin, mockDataPin, mockClockPin, direction);
    }
};

TEST_F(ShiftRegisterInputPinSetTest, openLatch_returns_false_if_latch_pin_processSignal_returns_false) {
    EXPECT_CALL(*mockLatchPin, processSignal(_)).WillRepeatedly(Return(false));

    EXPECT_FALSE(inputPinSet->openLatch());
}

TEST_F(ShiftRegisterInputPinSetTest, openLatch_returns_true_if_latch_pin_processSignal_returns_true) {
    EXPECT_CALL(*mockLatchPin, processSignal(_)).WillRepeatedly(Return(true));

    EXPECT_TRUE(inputPinSet->openLatch());
}

TEST_F(ShiftRegisterInputPinSetTest, closeLatch_returns_false_if_latch_pin_processSignal_returns_false) {
    EXPECT_CALL(*mockLatchPin, processSignal(_)).WillRepeatedly(Return(false));

    EXPECT_FALSE(inputPinSet->closeLatch());
}

TEST_F(ShiftRegisterInputPinSetTest, closeLatch_returns_true_if_latch_pin_processSignal_returns_true) {
    EXPECT_CALL(*mockLatchPin, processSignal(_)).WillRepeatedly(Return(true));

    EXPECT_TRUE(inputPinSet->closeLatch());
}

TEST_F(ShiftRegisterInputPinSetTest, shiftOut_calls_shiftOut_on_Arduino_interface) {
    const int value = 8;
    MockArduino mockArduino;
    setMockArduino(&mockArduino);
    ON_CALL(*mockDataPin, isConnected()).WillByDefault(Return(true));
    ON_CALL(*mockClockPin, isConnected()).WillByDefault(Return(true));

    EXPECT_CALL(mockArduino, _shiftOut(dataPinNum, clockPinNum, direction, value));

    EXPECT_TRUE(inputPinSet->shiftOut(value));

    setMockArduino(nullptr);
}

TEST_F(ShiftRegisterInputPinSetTest, shiftOut_returns_false_if_data_pin_is_not_connected) {
    const int value = 8;
    MockArduino mockArduino;
    setMockArduino(&mockArduino);
    ON_CALL(*mockDataPin, isConnected()).WillByDefault(Return(false));
    ON_CALL(*mockClockPin, isConnected()).WillByDefault(Return(true));

    EXPECT_FALSE(inputPinSet->shiftOut(value));

    setMockArduino(nullptr);
}

TEST_F(ShiftRegisterInputPinSetTest, shiftOut_returns_false_if_clock_pin_is_not_connected) {
    const int value = 8;
    MockArduino mockArduino;
    setMockArduino(&mockArduino);
    ON_CALL(*mockDataPin, isConnected()).WillByDefault(Return(true));
    ON_CALL(*mockClockPin, isConnected()).WillByDefault(Return(false));

    EXPECT_FALSE(inputPinSet->shiftOut(value));

    setMockArduino(nullptr);
}

TEST_F(ShiftRegisterInputPinSetTest, disconnect_calls_disconnect_on_each_pin) {
    EXPECT_CALL(*mockLatchPin, disconnect());
    EXPECT_CALL(*mockDataPin, disconnect());
    EXPECT_CALL(*mockClockPin, disconnect());

    inputPinSet->disconnect();
}

TEST_F(ShiftRegisterInputPinSetTest, size_returns_3) {
    EXPECT_EQ(inputPinSet->size(), 3);
}