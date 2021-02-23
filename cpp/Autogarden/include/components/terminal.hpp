#pragma once

#include <components/component.hpp>

class TerminalComponent : public Component
{
public:
    virtual ~TerminalComponent() = default;

protected:
    TerminalComponent(const std::string& id, IInputPinSet* inputPinSet) : Component(id), _pInputPinSet(inputPinSet) {}

    IOutputPinSet* _getOutputPins() override { return nullptr; }

protected:
    IInputPinSet* _pInputPinSet;
};
