#pragma once

#include <components/microcontroller/interfaces/factory.hpp>

class MicroControllerFactory : public IMicroControllerFactory {
public:
    std::unique_ptr<MicroController> create(const std::string& id, const std::initializer_list<int>& digitalOutputPins,
                                            const std::initializer_list<int>& digitalInputPins,
                                            const std::initializer_list<int>& analogOutputPins,
                                            const std::initializer_list<int>& analogInputPins) override {
        auto pinSet = buildTerminalPinSet(digitalOutputPins, digitalInputPins, analogOutputPins, analogInputPins);
        return std::make_unique<MicroController>(id, pinSet.release());
    }

    std::unique_ptr<ITerminalPinSet> buildTerminalPinSet(const std::initializer_list<int>& digitalOutputPins,
                                                         const std::initializer_list<int>& digitalInputPins,
                                                         const std::initializer_list<int>& analogOutputPins,
                                                         const std::initializer_list<int>& analogInputPins) {
        std::vector<std::unique_ptr<ITerminalPin>> pins;
        pins.reserve(digitalOutputPins.size() + digitalInputPins.size() + analogOutputPins.size() +
                     analogInputPins.size());
        addPins(digitalOutputPins, PinMode::DigitalOutput, &pins);
        addPins(digitalInputPins, PinMode::DigitalInput, &pins);
        addPins(analogOutputPins, PinMode::AnalogOutput, &pins);
        addPins(analogInputPins, PinMode::AnalogInput, &pins);
        return std::make_unique<TerminalPinSet>(std::move(pins));
    }

    void addPins(const std::initializer_list<int>& pinNums, const PinMode& pinMode,
                 std::vector<std::unique_ptr<ITerminalPin>>* pins) {
        for (const auto& pinNum : pinNums) {
            pins->emplace_back(new TerminalPin(pinNum, pinMode));
        }
    }
};
