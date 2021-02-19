#pragma once

#include <pins/interfaces/output_pinset.hpp>

template <typename T>
class OutputPinSet : virtual public IOutputPinSet {
public:
    OutputPinSet(std::vector<T>&& pins) : __mPins(std::move(pins)) {}

    virtual ~OutputPinSet() = default;

    bool connect(ILogicInputPinSet* inputPins) override {
        auto numSuccesses = 0;
        auto iter         = __mPins.begin();
        for (auto& pin : *inputPins) {
            numSuccesses += static_cast<int>(_connect(pin.get(), iter));
        }

        auto wasSuccessful = numSuccesses == inputPins->size();
        if (!wasSuccessful)
            inputPins->disconnect();

        return wasSuccessful;
    }

    bool connect(ILogicInputPin* pin) override {
        auto iter = __mPins.begin();
        return _connect(pin, iter);
    }

    int size() const override {
        return static_cast<int>(__mPins.size());
    }

protected:
    bool _connect(ILogicInputPin* pin, typename std::vector<T>::iterator& iter) {
        auto prev = pin->getOutputPin();
        while (iter != __mPins.end() && !pin->connect((*iter++).get())) continue;

        if (prev == pin->getOutputPin())
            return false;
        return true;
    }

protected:
    std::vector<T> __mPins;
};