#pragma once

#include <autogarden/interfaces/autogarden.hpp>

class IAutoGardenFactory {
public:
    virtual ~IAutoGardenFactory() = default;

    virtual std::unique_ptr<IAutoGarden> create() = 0;
};