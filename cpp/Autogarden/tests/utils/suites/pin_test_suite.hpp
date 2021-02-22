#pragma once

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <pins/interfaces/pin.hpp>

using namespace ::testing;

template <typename T>
class PinTestSuite : public Test {
protected:
    const int pinNum   = 1;
    const PinMode mode = PinMode::DigitalOutput;
    std::vector<PinMode> modes;
    std::unique_ptr<T> pin;

    void SetUp() {
        modes.push_back(PinMode::DigitalOutput);
        modes.push_back(PinMode::DigitalInput);
        modes.push_back(PinMode::AnalogOutput);
        modes.push_back(PinMode::AnalogInput);

        pin = std::make_unique<T>(pinNum, mode);
    }
};

TYPED_TEST_SUITE_P(PinTestSuite);

TYPED_TEST_P(PinTestSuite, getMode) {
    for (const auto& mode : this->modes) {
        this->pin = std::make_unique<TypeParam>(this->pinNum, mode);
        EXPECT_EQ(this->pin->getMode(), mode);
    }
}

TYPED_TEST_P(PinTestSuite, getPinNum) {
    EXPECT_EQ(this->pin->getPinNum(), this->pinNum);
}

TYPED_TEST_P(PinTestSuite, isConnected_is_initially_false) {
    EXPECT_FALSE(this->pin->isConnected());
}

REGISTER_TYPED_TEST_SUITE_P(PinTestSuite, getMode, getPinNum, isConnected_is_initially_false);