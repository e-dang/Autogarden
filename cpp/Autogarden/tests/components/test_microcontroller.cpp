#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <component_test_suite.hpp>
#include <components/microcontroller/microcontroller.hpp>
#include <mock_terminal.hpp>
#include <mock_terminal_pinset.hpp>

using namespace ::testing;

class MicroControllerTest : public Test {
protected:
    String id         = "controller";
    const int numPins = 8;
    std::vector<NiceMock<MockTerminalPin>> mockPins;
    NiceMock<MockTerminalPinSet>* mockPinSet;
    std::unique_ptr<MicroController> controller;

    MicroControllerTest() : mockPins(numPins), mockPinSet(new NiceMock<MockTerminalPinSet>()) {
        for (int i = 0; i < numPins; i++) {
            auto pin = &mockPins[i];
            ON_CALL(*mockPinSet, at(i)).WillByDefault(Return(pin));
        }
        ON_CALL(*mockPinSet, size()).WillByDefault(Return(numPins));

        controller = std::make_unique<MicroController>(id, mockPinSet);
    }
};

class MicroControllerFactory {
public:
    std::unique_ptr<MicroController> create() {
        return std::make_unique<MicroController>(id, new MockTerminalPinSet());
    }

    const String id = "testID";
};

INSTANTIATE_TYPED_TEST_SUITE_P(MicroController, ComponentTestSuite, MicroControllerFactory);

void AssertHasNoParent(const Component* obj) {
    EXPECT_FALSE(obj->hasParent());
    EXPECT_EQ(obj->getParent(), nullptr);
}

TEST_F(MicroControllerTest, controller_cannot_be_child_of_another_component) {
    auto otherController = std::make_shared<MicroController>("otherController", new MockTerminalPinSet());

    EXPECT_FALSE(controller->appendChild(otherController));
    AssertHasNoParent(otherController.get());
}

TEST_F(MicroControllerTest, controller_is_root_component) {
    EXPECT_TRUE(controller->isRoot());
}

TEST_F(MicroControllerTest, initialize_returns_true_if_initialization_of_all_pins_is_successful) {
    for (int i = 0; i < numPins; i++) {
        auto pin = &mockPins[i];
        EXPECT_CALL(*pin, initialize()).WillRepeatedly(Return(true));
    }

    EXPECT_TRUE(controller->initialize());
}

TEST_F(MicroControllerTest, initialize_returns_false_if_initialization_of_at_least_one_pins_is_unsuccessful) {
    for (int i = 0; i < numPins; i++) {
        auto pin = &mockPins[i];
        if (i > 0)
            EXPECT_CALL(*pin, initialize()).WillRepeatedly(Return(true));
        else
            EXPECT_CALL(*pin, initialize()).WillRepeatedly(Return(false));
    }

    EXPECT_FALSE(controller->initialize());
}