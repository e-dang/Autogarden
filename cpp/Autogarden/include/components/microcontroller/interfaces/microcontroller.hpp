#pragma once

#include <components/component.hpp>

class IMicroController : public Component {
public:
    IMicroController(const std::string& id) : Component(id) {}

    virtual ~IMicroController() = default;

    virtual bool initialize() = 0;
};