#pragma once

#include <gmock/gmock.h>

#include <client/interfaces/api_client.hpp>

class MockAPIClient : public IAPIClient {
public:
    MOCK_METHOD(DynamicJsonDocument, getWateringStationConfigs, (), (const, override));
    MOCK_METHOD(DynamicJsonDocument, getGardenConfigs, (), (const, override));
    MOCK_METHOD(void, sendGardenData, (const DynamicJsonDocument& data), (const, override));
    MOCK_METHOD(void, sendWateringStationData, (const DynamicJsonDocument& data), (const, override));
    MOCK_METHOD(int, getConnectionStrength, (), (const, override));
};