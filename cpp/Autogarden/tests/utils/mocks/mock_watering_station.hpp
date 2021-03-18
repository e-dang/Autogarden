#pragma once

#include <gmock/gmock.h>

#include <autogarden/interfaces/watering_station.hpp>

class MockWateringStation : public IWateringStation {
public:
    MOCK_METHOD(void, activate, (), (override));
    MOCK_METHOD(bool, update, (const JsonObject& configs), (override));
    MOCK_METHOD(int, getIdx, (), (const, override));
    MOCK_METHOD(JsonObjectConst, getData, (), (const, override));
};