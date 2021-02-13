#pragma once

#include <components/component.hpp>
#include <initializer_list>

class MicroController : public Component
{
public:
    MicroController(const std::string& id, ITerminalPinSet<DigitalPin>* digitalPins,
                    ITerminalPinSet<AnalogOutputPin>* analogOutputPins,
                    ITerminalPinSet<AnalogInputPin>* analogInputPins) :
        Component(id),
        __mDigitalPins(digitalPins),
        __mAnalogOutputPins(analogOutputPins),
        __mAnalogInputPins(analogInputPins)
    {
    }

    virtual ~MicroController() = default;

    void run() override { __mDigitalPins->refresh(); }

    bool hasNumAvailableOutputPins(const int& requestedNum, const PinMode& pinMode) override
    {
        if (pinMode == PinMode::Digital)
        {
            return requestedNum <= __mDigitalPins->getNumAvailable();
        }
        else if (pinMode == PinMode::AnalogOutput)
        {
            return requestedNum <= __mAnalogOutputPins->getNumAvailable();
        }
        else if (pinMode == PinMode::AnalogInput)
        {
            return requestedNum <= __mAnalogInputPins->getNumAvailable();
        }

        return false;
    }

    std::vector<PinView> getNumAvailableOutputPins(const int& requestedNum, const PinMode& pinMode) override
    {
        if (pinMode == PinMode::Digital)
        {
            return __mDigitalPins->getNextAvailable(requestedNum);
        }
        else if (pinMode == PinMode::AnalogOutput)
        {
            return __mAnalogOutputPins->getNextAvailable(requestedNum);
        }
        else if (pinMode == PinMode::AnalogInput)
        {
            return __mAnalogInputPins->getNextAvailable(requestedNum);
        }

        return std::vector<PinView>();
    }

    std::vector<uint8_t> getDigitalPinNums() const { return __mDigitalPins->getPinNumbers(); }

    std::vector<uint8_t> getAnalogOutputPinNums() const { return __mAnalogOutputPins->getPinNumbers(); }

    std::vector<uint8_t> getAnalogInputPinNums() const { return __mAnalogInputPins->getPinNumbers(); }

    int getAvailableDigitalPins() const { return __mDigitalPins->getNumAvailable(); }

    int getAvailableAnalogOutputPins() const { return __mAnalogOutputPins->getNumAvailable(); }

    int getAvailableAnalogInputPins() const { return __mAnalogInputPins->getNumAvailable(); }

protected:
    bool _setInputPins(Component* component) override
    {
        return false;  // MicroController doesn't have any inputs. This makes it so it is always the root of the tree.
    }

private:
    ITerminalPinSet<DigitalPin>* __mDigitalPins;
    ITerminalPinSet<AnalogOutputPin>* __mAnalogOutputPins;
    ITerminalPinSet<AnalogInputPin>* __mAnalogInputPins;
};

class MicroControllerFactory
{
public:
    std::unique_ptr<MicroController> createMicroController(const std::string& id,
                                                           const std::initializer_list<uint8_t>& digital,
                                                           const std::initializer_list<uint8_t>& analogOutput,
                                                           const std::initializer_list<uint8_t>& analogInput)
    {
        auto digitalPins      = createTerminalPinSet<DigitalPin>(digital);
        auto analogOutputPins = createTerminalPinSet<AnalogOutputPin>(analogOutput);
        auto analogInputPins  = createTerminalPinSet<AnalogInputPin>(analogInput);
        return std::make_unique<MicroController>(id, digitalPins, analogOutputPins, analogInputPins);
    }
};
