#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/microcontroller/microcontroller.hpp>
#include <mock_terminal_pinset.hpp>

using namespace ::testing;

class MicroControllerTest : public Test {
protected:
    std::string id = "controller";
    MockTerminalPinSet mockPinSet;
    MicroController controller;

    MicroControllerTest() : mockPinSet(), controller(id, &mockPinSet) {}
};

void AssertHasNoParent(const Component* obj) {
    EXPECT_FALSE(obj->hasParent());
    EXPECT_EQ(obj->getParent(), nullptr);
}

TEST_F(MicroControllerTest, getId) {
    EXPECT_EQ(controller.getId(), id);
}

TEST_F(MicroControllerTest, controller_initially_has_no_children) {
    EXPECT_EQ(controller.getNumChildren(), 0);
}

TEST_F(MicroControllerTest, controller_has_no_parent) {
    AssertHasNoParent(&controller);
}

TEST_F(MicroControllerTest, getChild_returns_nullptr_when_no_child_is_found) {
    EXPECT_EQ(controller.getChild("dne"), nullptr);
}

TEST_F(MicroControllerTest, controller_cannot_be_child_of_another_component) {
    MockTerminalPinSet otherMockPinSet;
    MicroController otherController("otherController", &otherMockPinSet);

    EXPECT_FALSE(controller.appendChild(&otherController));
    AssertHasNoParent(&otherController);
}