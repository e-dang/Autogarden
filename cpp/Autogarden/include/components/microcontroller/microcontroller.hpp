#pragma once

#include <components/component.hpp>

class MicroController : public Component {
public:
    MicroController(const std::string& id, ITerminalPinSet* pins) : Component(id), __mPins(pins) {}

protected:
    bool _setInputPins(IOutputPinSet* outputPins) override {
        return false;
    }

    IOutputPinSet* _getOutputPins() override {
        return __mPins;
    }

    bool _propagateSignal() override {
        return true;
    }

private:
    ITerminalPinSet* __mPins;
};