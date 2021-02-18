#pragma once

#include <components/component.hpp>

class MicroController : public Component {
public:
    MicroController(const std::string& id, ITerminalPinSet* pins) : Component(id), __mPins(pins) {
        _pRoot = this;
    }

    IOutputPinSet* getOutputPins() override {
        return __mPins.get();
    }

protected:
    bool _setInputPins(Component* parent) override {
        return false;
    }

    bool _propagateSignal() override {
        return true;
    }

private:
    std::unique_ptr<ITerminalPinSet> __mPins;
};