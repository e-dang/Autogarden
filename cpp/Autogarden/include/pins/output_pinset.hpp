#pragma once

#include <pins/interfaces/output_pinset.hpp>

template <typename T>
class OutputPinSet : virtual public IOutputPinSet {
public:
    OutputPinSet(std::vector<T>&& pins) : __mPins(std::move(pins)) {}

    virtual ~OutputPinSet() = default;

    void connect(ILogicInputPinSet* inputPins) override {
        auto iter = __mPins.begin();
        for (auto& pin : *inputPins) {
            _connect(pin.get(), iter);
        }
    }

    void connect(ILogicInputPin* pin) override {
        auto iter = __mPins.begin();
        _connect(pin, iter);
    }

    int size() const override {
        return static_cast<int>(__mPins.size());
    }

protected:
    void _connect(ILogicInputPin* pin, typename std::vector<T>::iterator& iter) {
        while (iter != __mPins.end() && !pin->connect((*iter++).get())) continue;
    }

protected:
    std::vector<T> __mPins;
};