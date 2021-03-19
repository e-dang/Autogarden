#pragma once

#include <components/component.hpp>

class ILiquidLevelSensor : public Component {
public:
    ILiquidLevelSensor() = default;

    ILiquidLevelSensor(const String& id) : Component(id) {}

    virtual ~ILiquidLevelSensor() = default;

    virtual const char* read() = 0;

public:
    const char* const OK_VALUE  = "ok";
    const char* const LOW_VALUE = "lo";
};