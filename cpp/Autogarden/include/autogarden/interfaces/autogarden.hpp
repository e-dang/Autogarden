#pragma once

#include <ArduinoJson.h>

class IAutoGarden {
public:
    virtual ~IAutoGarden() = default;

    virtual bool initializePins() = 0;

    virtual void initializeServer() = 0;

    virtual void refreshWateringStations() = 0;

    virtual void run() = 0;
};