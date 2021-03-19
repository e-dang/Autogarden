#pragma once

#include <ArduinoJson.h>

class IAutoGarden {
public:
    virtual ~IAutoGarden() = default;

    virtual bool initialize() = 0;

    virtual void run() = 0;
};