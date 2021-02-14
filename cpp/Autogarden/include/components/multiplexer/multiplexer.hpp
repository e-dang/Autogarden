#pragma once

#include <components/connector.hpp>
#include <components/multiplexer/oi_policy.hpp>
#include <components/multiplexer/output_pin_set.hpp>
#include <pins/pins.hpp>

class Multiplexer : public ConnectorComponent {
public:
    Multiplexer(const std::string& id, IInputPinSet* logicInputPins, IOutputPinSet* outputPins,
                IOutputToInputPolicy* policy, const PinMode& sigPinMode) :
        ConnectorComponent(id, logicInputPins, outputPins),
        __pPolicy(policy),
        __mSigPinMode(sigPinMode),
        __mSigPin(nullptr),
        __mEnablePin(nullptr) {}

    virtual ~Multiplexer() = default;

    void run() override {
        if (_pParent == nullptr)
            throw std::runtime_error("Component " + getId() + " doesn't have a parent");

        if (__pPolicy->execute(_pInputPinSet, _pOutputPinSet))
            enable();
        else
            disable();

        _pParent->run();
    }

    bool enable() {
        return _setPinView(__mEnablePin, LOW);
    }

    bool disable() {
        return _setPinView(__mEnablePin, HIGH);
    }

    bool setSigPin(const int& value) {
        return _setPinView(__mSigPin, value);
    }

    PinMode getSigPinMode() const {
        return __mSigPinMode;
    }

protected:
    bool _setInputPins(IOutputPinSet* parentOutputPins) override {
        if (parentOutputPins == nullptr)
            return false;

        if (_pInputPinSet->getMode() == getSigPinMode()) {
            const auto requiredNumOutputs = _pInputPinSet->size() + 1;
            if (parentOutputPins->hasNumAvailable(requiredNumOutputs, _pInputPinSet->getMode())) {
                _pInputPinSet->connectToOutput(
                  parentOutputPins->getNextAvailable(requiredNumOutputs - 1, _pInputPinSet->getMode()));
                __mSigPin    = parentOutputPins->getNextAvailable(1, getSigPinMode()).front();
                __mEnablePin = parentOutputPins->getNextAvailable(1, PinMode::Digital).front();
                disable();
                return true;
            }
        } else {
            if (parentOutputPins->hasNumAvailable(_pInputPinSet->size(), _pInputPinSet->getMode()) &&
                parentOutputPins->hasNumAvailable(1, getSigPinMode())) {
                _pInputPinSet->connectToOutput(
                  parentOutputPins->getNextAvailable(_pInputPinSet->size(), _pInputPinSet->getMode()));
                __mSigPin    = parentOutputPins->getNextAvailable(1, getSigPinMode()).front();
                __mEnablePin = parentOutputPins->getNextAvailable(1, PinMode::Digital).front();
                disable();
                return true;
            }
        }

        return false;
    }

    IOutputPinSet* _getOutputPins() override {
        return _pOutputPinSet;
    }

    bool _setPinView(PinView& pinView, const int& value) {
        if (!pinView.isNull) {
            pinView.set(value);
            return true;
        }
        return false;
    }

private:
    PinMode __mSigPinMode;
    PinView __mSigPin;
    PinView __mEnablePin;
    IOutputToInputPolicy* __pPolicy;
};

class MultiplexerFactory {
public:
    std::vector<IPin*> createPin(const int& numPins) {
        std::vector<IPin*> pins;
        pins.reserve(numPins);
        for (int i = 0; i < numPins; i++) {
            pins.push_back(new LogicPin(i, PinMode::Digital));
        }
        return pins;
    }

    Multiplexer* createMultiplexer(const std::string& id, const int& numLogicInputPins, const int& numOutputPins,
                                   const PinMode& sigPinMode) {
        auto logicInputPins = __mInputFactory.createInputPinSet(numLogicInputPins, PinMode::Digital);
        auto outputPins     = new MultiplexerOutputPinSet(createPin(numOutputPins));
        auto policy         = new MultiplexerOIPolicy();
        return new Multiplexer(id, logicInputPins, outputPins, policy, sigPinMode);
    }

private:
    InputPinSetFactory __mInputFactory;
};