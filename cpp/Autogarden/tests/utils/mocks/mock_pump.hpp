#pragma once

#include <gmock/gmock.h>

#include <components/pump/pump.hpp>

class MockPump : public IPump {
public:
    MOCK_METHOD(bool, start, (), (override));
    MOCK_METHOD(bool, stop, (), (override));
};