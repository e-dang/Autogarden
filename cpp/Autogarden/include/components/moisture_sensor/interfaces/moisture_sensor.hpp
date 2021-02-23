#pragma once

#include <components/component.hpp>

class IMoistureSensor : public Component {
public:
    IMoistureSensor() = default;

    IMoistureSensor(const String& id) : Component(id) {}

    virtual ~IMoistureSensor() = default;

    virtual int readRaw() = 0;

    virtual float readScaled() = 0;
};