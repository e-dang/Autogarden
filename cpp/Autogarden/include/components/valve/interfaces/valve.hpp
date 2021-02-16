#pragma once

#include <components/component.hpp>

class IValve : virtual public Component {
public:
    virtual ~IValve() = default;

    virtual bool open() = 0;

    virtual bool close() = 0;
};