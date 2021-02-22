#pragma once

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/component.hpp>

using namespace ::testing;

template <typename T>
class ComponentTestSuite : public Test {
protected:
    T factory;
};

TYPED_TEST_SUITE_P(ComponentTestSuite);

TYPED_TEST_P(ComponentTestSuite, getId) {
    auto component = this->factory.create();
    EXPECT_EQ(component->getId(), this->factory.id);
}

TYPED_TEST_P(ComponentTestSuite, component_initially_has_no_children) {
    auto component = this->factory.create();
    EXPECT_EQ(component->getNumChildren(), 0);
}

TYPED_TEST_P(ComponentTestSuite, component_initially_has_no_parent) {
    auto component = this->factory.create();
    EXPECT_FALSE(component->hasParent());
    EXPECT_EQ(component->getParent(), nullptr);
}

TYPED_TEST_P(ComponentTestSuite, getChild_returns_nullptr_when_no_child_is_found) {
    auto component = this->factory.create();
    EXPECT_EQ(component->getChild("dne"), nullptr);
}

REGISTER_TYPED_TEST_SUITE_P(ComponentTestSuite, getId, component_initially_has_no_children,
                            component_initially_has_no_parent, getChild_returns_nullptr_when_no_child_is_found);