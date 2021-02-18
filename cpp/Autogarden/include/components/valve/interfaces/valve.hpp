#pragma once

#include <components/component.hpp>

class IValve : public Component {
public:
    IValve(const std::string& id) : Component(id) {}

    virtual ~IValve() = default;

    virtual bool open() = 0;

    virtual bool close() = 0;
};