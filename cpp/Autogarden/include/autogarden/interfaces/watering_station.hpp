#pragma once

#include <ArduinoJson.h>

class IWateringStation {
public:
    virtual ~IWateringStation() = default;

    virtual void activate() = 0;

    virtual bool update(const DynamicJsonDocument& configs) = 0;

    virtual int getIdx() const = 0;
};