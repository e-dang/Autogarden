#pragma once

#include <components/component.hpp>

class ConnectorComponent : public Component {
public:
    virtual ~ConnectorComponent() = default;

protected:
    ConnectorComponent(const std::string& id, IInputPinSet* inputPinSet, IOutputPinSet* outputPinSet) :
        Component(id), _pInputPinSet(inputPinSet), _pOutputPinSet(outputPinSet) {}

protected:
    IInputPinSet* _pInputPinSet;
    IOutputPinSet* _pOutputPinSet;
};
