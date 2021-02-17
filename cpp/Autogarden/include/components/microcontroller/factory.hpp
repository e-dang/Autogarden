#pragma once

#include <components/microcontroller/interfaces/factory.hpp>

class MicroControllerFactory : public IMicroControllerFactory {
public:
    std::unique_ptr<MicroController> create(const std::string& id,
                                            const std::initializer_list<int>& digitalOutputPinsNums,
                                            const std::initializer_list<int>& digitalInputPinNums,
                                            const std::initializer_list<int>& analogOutputPinNums,
                                            const std::initializer_list<int>& analogInputPinNums) override {
        std::vector<std::vector<std::unique_ptr<typename TerminalPinSet::value_type>>> vec;
        vec.reserve(static_cast<int>(PinMode::Count));
        vec.emplace_back(__mTerminalPinSetFactory.createPinVector(digitalOutputPinsNums, PinMode::DigitalOutput));
        vec.emplace_back(__mTerminalPinSetFactory.createPinVector(digitalInputPinNums, PinMode::DigitalInput));
        vec.emplace_back(__mTerminalPinSetFactory.createPinVector(analogOutputPinNums, PinMode::AnalogOutput));
        vec.emplace_back(__mTerminalPinSetFactory.createPinVector(analogInputPinNums, PinMode::AnalogInput));
        auto pinSet = __mTerminalPinSetFactory.createPinSet(vec);
        return std::make_unique<MicroController>(id, pinSet.release());
    }

private:
    PinFactory<TerminalPinSet, TerminalPin> __mTerminalPinSetFactory;
};
