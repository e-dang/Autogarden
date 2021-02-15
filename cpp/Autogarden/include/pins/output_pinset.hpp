#pragma once

#include <pins/interfaces/output_pinset.hpp>

template <typename T>
class OutputPinSet : virtual public IOutputPinSet {
public:
    OutputPinSet(std::vector<T> pins) : __mPins(pins) {}

    virtual ~OutputPinSet() = default;

    void connect(ILogicInputPinSet* inputPins) override {
        iter = __mPins.begin();
        for (auto& pin : *inputPins) {
            _connect(pin);
        }
    }

    void connect(ILogicInputPin* pin) override {
        iter = __mPins.begin();
        _connect(pin);
    }

    int size() const override {
        return static_cast<int>(__mPins.size());
    }

protected:
    void _connect(ILogicInputPin* pin) {
        while (iter != __mPins.end() && !pin->connect(*iter++)) continue;
    }

protected:
    std::vector<T> __mPins;
    typename std::vector<T>::iterator iter;
};