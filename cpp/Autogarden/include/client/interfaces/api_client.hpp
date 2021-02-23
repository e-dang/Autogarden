#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>

class IAPIClient {
public:
    virtual ~IAPIClient() = default;

    virtual void initializeServer(const DynamicJsonDocument& request) = 0;

    virtual DynamicJsonDocument fetchConfigs() = 0;

    virtual String getWateringStationsUrl() const = 0;

    virtual String getInitializationUrl() const = 0;
};

class IAPIClientFactory {
public:
    virtual ~IAPIClientFactory() = default;

    virtual std::unique_ptr<IAPIClient> create(const String& ssid, const String& password, const String& rootUrl,
                                               const int& waitTime = 1000) = 0;
};