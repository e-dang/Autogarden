#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>

class IAPIClient {
public:
    virtual ~IAPIClient() = default;

    virtual DynamicJsonDocument getWateringStationConfigs() const = 0;

    virtual DynamicJsonDocument getGardenConfigs() const = 0;

    virtual void sendGardenData(const DynamicJsonDocument& data) const = 0;

    virtual void sendWateringStationData(const DynamicJsonDocument& data) const = 0;

    virtual int getConnectionStrength() const = 0;
};

class IAPIClientFactory {
public:
    virtual ~IAPIClientFactory() = default;

    virtual std::unique_ptr<IAPIClient> create(const String& apiKey, const String& ssid, const String& password,
                                               const String& rootUrl, const int& waitTime = 1000) = 0;
};