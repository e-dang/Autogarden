#pragma once

#include <gmock/gmock.h>

#include <components/valve/valve.hpp>

class MockValve : public IValve {
public:
    MOCK_METHOD(bool, open, (), (override));
    MOCK_METHOD(bool, close, (), (override));
};