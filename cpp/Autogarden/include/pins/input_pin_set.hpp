#pragma once

#include <pins/pin_set.hpp>
#include <pins/pin_view.hpp>
#include <vector>

class IInputPinSet : public PinSet {
public:
    virtual ~IInputPinSet() = default;

    virtual bool connectToOutput(std::vector<PinView>&& outputPins) = 0;

    virtual void setPin(const int& idx, const int& value) = 0;

    virtual PinMode getMode() const = 0;
};

class InputPinSet : public IInputPinSet {
public:
    InputPinSet(std::vector<PinView>&& pinViews, const PinMode& pinMode) :
        _mPins(std::move(pinViews)), _mPinMode(pinMode) {}

    virtual ~InputPinSet() = default;

    bool connectToOutput(std::vector<PinView>&& outputPins) override {
        if (outputPins.size() != size())
            return false;

        _mPins = outputPins;
        return true;
    }

    virtual void setPin(const int& idx, const int& value) override {
        _mPins.at(idx).set(value);
    }

    PinMode getMode() const override {
        return _mPinMode;
    }

    int size() const override {
        return static_cast<int>(_mPins.size());
    }

protected:
    PinMode _mPinMode;
    std::vector<PinView> _mPins;
};

class InputPinSetFactory {
public:
    std::vector<PinView> createPinViews(const int& numInputPins) {
        return std::vector<PinView>(numInputPins, PinView(nullptr));
    }

    IInputPinSet* createInputPinSet(const int& numInputPins, const PinMode& pinMode) {
        return new InputPinSet(createPinViews(numInputPins), pinMode);
    }
};