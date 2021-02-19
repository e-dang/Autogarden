#pragma once

#include <components/component.hpp>

class MicroController : public Component {
public:
    MicroController(const std::string& id, ITerminalPinSet* pins) : Component(id), __mPins(pins) {
        _pRoot = this;
    }

protected:
    bool _setInputPins(Component* parent) override {
        return false;
    }

    IOutputPinSet* _getOutputPins() override {
        return __mPins.get();
    }

    bool _propagateSignal() override {
        return true;
    }

private:
    std::unique_ptr<ITerminalPinSet> __mPins;
};