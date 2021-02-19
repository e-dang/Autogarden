#pragma once

#include <components/microcontroller/interfaces/microcontroller.hpp>
#include <memory>

class IMicroControllerFactory {
public:
    ~IMicroControllerFactory() = default;

    virtual std::unique_ptr<IMicroController> create(const std::string& id,
                                                     const std::initializer_list<int>& digitalOutputPins,
                                                     const std::initializer_list<int>& digitalInputPins,
                                                     const std::initializer_list<int>& analogOutputPins,
                                                     const std::initializer_list<int>& analogInputPins) = 0;
};