#pragma once

#include <gmock/gmock.h>

#include <autogarden/config_parser.hpp>

class MockWateringStationConfigParser : public IWateringStationConfigParser<WateringStationConfigs> {
public:
    MOCK_METHOD(WateringStationConfigs, parse, (const DynamicJsonDocument& configs), (override));
};