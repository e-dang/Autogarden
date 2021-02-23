#pragma once

#include <gmock/gmock.h>

#include <client/interfaces/api_client.hpp>

class MockAPIClient : public IAPIClient {
public:
    MOCK_METHOD(void, initializeServer, (const DynamicJsonDocument& request), (override));
    MOCK_METHOD(DynamicJsonDocument, fetchConfigs, (), (override));
    MOCK_METHOD(String, getWateringStationsUrl, (), (const, override));
    MOCK_METHOD(String, getInitializationUrl, (), (const, override));
};