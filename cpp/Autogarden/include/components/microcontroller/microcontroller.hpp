#pragma once

#include <components/microcontroller/interfaces/microcontroller.hpp>

class MicroController : public IMicroController {
public:
    MicroController(const std::string& id, ITerminalPinSet* pins) : IMicroController(id), __mPins(pins) {
        _pRoot = this;
    }

    bool initialize() override {
        auto numSuccesses = 0;
        for (int i = 0; i < __mPins->size(); i++) {
            numSuccesses += static_cast<int>(__mPins->at(i)->initialize());
        }

        return numSuccesses == __mPins->size();
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