#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <component_test_suite.hpp>
#include <components/shift_register/shift_register.hpp>
#include <mock_logic_output_pinset.hpp>
#include <mock_shift_register_input_pinset.hpp>

class ShiftRegisterFactory {
public:
    std::unique_ptr<ShiftRegister> create() {
        return std::make_unique<ShiftRegister>(id, new MockShiftRegisterInputPinSet(), new MockLogicOutputPinSet());
    }

    const String id = "testID";
};

INSTANTIATE_TYPED_TEST_SUITE_P(ShiftRegister, ComponentTestSuite, ShiftRegisterFactory);