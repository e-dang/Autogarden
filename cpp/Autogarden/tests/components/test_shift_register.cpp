#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/shift_register/shift_register.hpp>
#include <mocks/mock_logic_output_pinset.hpp>
#include <mocks/mock_shift_register_input_pinset.hpp>
#include <suites/component_test_suite.hpp>

class ShiftRegisterFactory {
public:
    std::unique_ptr<ShiftRegister> create() {
        return std::make_unique<ShiftRegister>(id, new MockShiftRegisterInputPinSet(), new MockLogicOutputPinSet());
    }

    const String id = "testID";
};

INSTANTIATE_TYPED_TEST_SUITE_P(ShiftRegister, ComponentTestSuite, ShiftRegisterFactory);