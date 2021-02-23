#pragma once

#include <functional>
#include <pins/logic_input.hpp>
#include <pins/logic_input_pinset.hpp>
#include <pins/logic_output.hpp>
#include <pins/logic_output_pinset.hpp>
#include <pins/terminal.hpp>
#include <pins/terminal_pinset.hpp>

class IPinFactory {
public:
    virtual ~IPinFactory() = default;

    virtual std::unique_ptr<ITerminalPin> createTerminalPin(const int& pinNum, const PinMode& pinMode) = 0;

    virtual std::unique_ptr<ILogicOutputPin> createLogicOutputPin(const int& pinNum, const PinMode& pinMode) = 0;

    virtual std::unique_ptr<ILogicInputPin> createLogicInputPin(const int& pinNum, const PinMode& pinMode) = 0;

    virtual std::unique_ptr<ITerminalPinSet> createTerminalPinSet(const std::initializer_list<int>& pinNums,
                                                                  const PinMode& pinMode)                     = 0;
    virtual std::unique_ptr<ITerminalPinSet> createTerminalPinSet(const int& numPins, const PinMode& pinMode) = 0;

    virtual std::unique_ptr<ILogicOutputPinSet> createLogicOutputPinSet(const std::initializer_list<int>& pinNums,
                                                                        const PinMode& pinMode)                     = 0;
    virtual std::unique_ptr<ILogicOutputPinSet> createLogicOutputPinSet(const int& numPins, const PinMode& pinMode) = 0;

    virtual std::unique_ptr<ILogicInputPinSet> createLogicInputPinSet(const std::initializer_list<int>& pinNums,
                                                                      const PinMode& pinMode)                     = 0;
    virtual std::unique_ptr<ILogicInputPinSet> createLogicInputPinSet(const int& numPins, const PinMode& pinMode) = 0;
};

class PinFactory : public IPinFactory {
public:
    std::unique_ptr<ITerminalPin> createTerminalPin(const int& pinNum, const PinMode& pinMode) override {
        return std::make_unique<TerminalPin>(pinNum, pinMode);
    }

    std::unique_ptr<ILogicOutputPin> createLogicOutputPin(const int& pinNum, const PinMode& pinMode) override {
        return std::make_unique<LogicOutputPin>(pinNum, pinMode);
    }

    std::unique_ptr<ILogicInputPin> createLogicInputPin(const int& pinNum, const PinMode& pinMode) override {
        return std::make_unique<LogicInputPin>(pinNum, pinMode);
    }

    std::unique_ptr<ITerminalPinSet> createTerminalPinSet(const std::initializer_list<int>& pinNums,
                                                          const PinMode& pinMode) override {
        auto createPin = [this](const int& pinNum, const PinMode& pinMode) {
            return this->createTerminalPin(pinNum, pinMode);
        };

        return __createPinSet<TerminalPinSet, ITerminalPin>(pinNums, pinMode, createPin);
    }

    std::unique_ptr<ITerminalPinSet> createTerminalPinSet(const int& numPins, const PinMode& pinMode) override {
        auto createPin = [this](const int& pinNum, const PinMode& pinMode) {
            return this->createTerminalPin(pinNum, pinMode);
        };
        return __createPinSet<TerminalPinSet, ITerminalPin>(numPins, pinMode, createPin);
    }

    std::unique_ptr<ILogicOutputPinSet> createLogicOutputPinSet(const std::initializer_list<int>& pinNums,
                                                                const PinMode& pinMode) override {
        auto createPin = [this](const int& pinNum, const PinMode& pinMode) {
            return this->createLogicOutputPin(pinNum, pinMode);
        };
        return __createPinSet<LogicOutputPinSet, ILogicOutputPin>(pinNums, pinMode, createPin);
    }

    std::unique_ptr<ILogicOutputPinSet> createLogicOutputPinSet(const int& numPins, const PinMode& pinMode) override {
        auto createPin = [this](const int& pinNum, const PinMode& pinMode) {
            return this->createLogicOutputPin(pinNum, pinMode);
        };
        return __createPinSet<LogicOutputPinSet, ILogicOutputPin>(numPins, pinMode, createPin);
    }

    std::unique_ptr<ILogicInputPinSet> createLogicInputPinSet(const std::initializer_list<int>& pinNums,
                                                              const PinMode& pinMode) override {
        auto createPin = [this](const int& pinNum, const PinMode& pinMode) {
            return this->createLogicInputPin(pinNum, pinMode);
        };
        return __createPinSet<LogicInputPinSet, ILogicInputPin>(pinNums, pinMode, createPin);
    }

    std::unique_ptr<ILogicInputPinSet> createLogicInputPinSet(const int& numPins, const PinMode& pinMode) override {
        auto createPin = [this](const int& pinNum, const PinMode& pinMode) {
            return this->createLogicInputPin(pinNum, pinMode);
        };
        return __createPinSet<LogicInputPinSet, ILogicInputPin>(numPins, pinMode, createPin);
    }

private:
    template <typename T, typename U>
    std::unique_ptr<T> __createPinSet(const std::initializer_list<int>& pinNums, const PinMode& pinMode,
                                      std::function<std::unique_ptr<U>(const int&, const PinMode&)> createPin) {
        std::vector<std::unique_ptr<U>> pins;
        pins.reserve(pinNums.size());
        for (const auto& pinNum : pinNums) {
            pins.emplace_back(createPin(pinNum, pinMode));
        }
        return std::make_unique<T>(std::move(pins));
    }

    template <typename T, typename U>
    std::unique_ptr<T> __createPinSet(const int& numPins, const PinMode& pinMode,
                                      std::function<std::unique_ptr<U>(const int&, const PinMode&)> createPin) {
        std::vector<std::unique_ptr<U>> pins;
        pins.reserve(numPins);
        for (int i = 0; i < numPins; i++) {
            pins.emplace_back(createPin(i, pinMode));
        }
        return std::make_unique<T>(std::move(pins));
    }
};