#pragma once

#include <ArduinoJson.h>

template <typename T>
class IWateringStationConfigParser {
public:
    virtual ~IWateringStationConfigParser() = default;

    virtual T parse(const JsonObject& configs) = 0;
};