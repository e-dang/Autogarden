#pragma once

#include <components/component.hpp>

class IMicroController : public Component {
public:
    IMicroController() = default;

    IMicroController(const String& id) : Component(id) {}

    virtual ~IMicroController() = default;

    virtual bool initialize() = 0;
};