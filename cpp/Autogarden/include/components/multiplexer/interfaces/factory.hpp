#pragma once

#include <components/multiplexer/interfaces/multiplexer.hpp>

class IMultiplexerFactory {
public:
    virtual ~IMultiplexerFactory() = default;

    virtual std::unique_ptr<IMultiplexer> create(const std::string& id, const int& numLogicInputs,
                                                 const int& numOutputs, const PinMode& sigMode) = 0;
};