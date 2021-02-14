#pragma once

#include <components/component.hpp>
#include <initializer_list>

class MicroController : public Component {
public:
    MicroController(const std::string& id, ITerminalPinSet* pins) : Component(id), __pPins(pins) {}

    virtual ~MicroController() = default;

    void run() override {
        __pPins->refresh();
    }

protected:
    bool _setInputPins(IOutputPinSet* parentOutputPins) override {
        return false;  // MicroController doesn't have any inputs. This makes it so it is always the root of the tree.
    }

    IOutputPinSet* _getOutputPins() override {
        return __pPins;
    }

private:
    ITerminalPinSet* __pPins;
};

class MicroControllerFactory {
public:
    template <typename T>
    void createPins(std::vector<ITerminalPin*>& pins, const std::initializer_list<uint8_t>& pinNums) {
        for (const auto& pinNum : pinNums) {
            pins.push_back(new T(pinNum));
        }
    }

    std::unique_ptr<MicroController> createMicroController(const std::string& id,
                                                           const std::initializer_list<uint8_t>& digital,
                                                           const std::initializer_list<uint8_t>& analogOutput,
                                                           const std::initializer_list<uint8_t>& analogInput) {
        std::vector<ITerminalPin*> pins;
        pins.reserve(digital.size() + analogOutput.size() + analogInput.size());
        createPins<DigitalPin>(pins, digital);
        createPins<AnalogOutputPin>(pins, digital);
        createPins<AnalogInputPin>(pins, digital);
        auto pinSet = new TerminalPinSet(std::move(pins));
        return std::make_unique<MicroController>(id, pinSet);
    }
};
