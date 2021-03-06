#pragma once

#include <components/liquid_level_sensor/liquid_level_sensor.hpp>
#include <components/microcontroller/microcontroller.hpp>
#include <components/moisture_sensor/moisture_sensor.hpp>
#include <components/multiplexer/multiplexer.hpp>
#include <components/multiplexer/translation_policy.hpp>
#include <components/pump/pump.hpp>
#include <components/shift_register/shift_register.hpp>
#include <components/valve/valve.hpp>
#include <pins/factory.hpp>
#include <signals/factory.hpp>

class IComponentFactory {
public:
    virtual ~IComponentFactory() = default;

    virtual std::unique_ptr<IMicroController> createMicroController(
      const String& id, const std::initializer_list<int>& digitalOutputPinsNums,
      const std::initializer_list<int>& digitalInputPinNums, const std::initializer_list<int>& analogOutputPinNums,
      const std::initializer_list<int>& analogInputPinNums) = 0;

    virtual std::shared_ptr<IShiftRegister> createShiftRegister(const String& id, const int& numOutputPins,
                                                                const int& direction) = 0;

    virtual std::shared_ptr<IMultiplexer> createMultiplexer(const String& id, const int& numLogicInputs,
                                                            const int& numOutputs, const PinMode& sigMode) = 0;

    virtual std::shared_ptr<IValve> createValve(const String& id, const int& onValue, const int& offValue) = 0;

    virtual std::shared_ptr<IMoistureSensor> createMoistureSensor(const String& id, const float& scaler) = 0;

    virtual std::shared_ptr<IPump> createPump(const String& id, const int& onValue, const int& offValue) = 0;

    virtual std::shared_ptr<ILiquidLevelSensor> createLiquidLevelSensor(const String& id, const int& okValue) = 0;
};

class ComponentFactory : public IComponentFactory {
public:
    ComponentFactory(std::unique_ptr<ISignalFactory>&& signalFactory, std::unique_ptr<IPinFactory>&& pinFactory) :
        __pSignalFactory(std::move(signalFactory)), __pPinFactory(std::move(pinFactory)) {}

    std::unique_ptr<IMicroController> createMicroController(
      const String& id, const std::initializer_list<int>& digitalOutputPinsNums,
      const std::initializer_list<int>& digitalInputPinNums, const std::initializer_list<int>& analogOutputPinNums,
      const std::initializer_list<int>& analogInputPinNums) override {
        auto pinSet1 = __pPinFactory->createTerminalPinSet(digitalOutputPinsNums, PinMode::DigitalOutput);
        auto pinSet2 = __pPinFactory->createTerminalPinSet(digitalInputPinNums, PinMode::DigitalInput);
        auto pinSet3 = __pPinFactory->createTerminalPinSet(analogOutputPinNums, PinMode::AnalogOutput);
        auto pinSet4 = __pPinFactory->createTerminalPinSet(analogInputPinNums, PinMode::AnalogInput);
        pinSet1->merge(std::move(pinSet2));
        pinSet1->merge(std::move(pinSet3));
        pinSet1->merge(std::move(pinSet4));

        return std::make_unique<MicroController>(id, pinSet1.release());
    }

    std::shared_ptr<IShiftRegister> createShiftRegister(const String& id, const int& numOutputPins,
                                                        const int& direction) override {
        auto logicPin = __pPinFactory->createLogicInputPin(0, PinMode::DigitalOutput);
        auto dataPin  = __pPinFactory->createLogicInputPin(1, PinMode::DigitalOutput);
        auto clockPin = __pPinFactory->createLogicInputPin(2, PinMode::DigitalOutput);
        auto inputPinSet =
          new ShiftRegisterInputPinSet(logicPin.release(), dataPin.release(), clockPin.release(), direction);

        auto outputPinSet = __pPinFactory->createLogicOutputPinSet(numOutputPins, PinMode::DigitalOutput);
        return std::make_shared<ShiftRegister>(id, inputPinSet, outputPinSet.release());
    }

    std::shared_ptr<IMultiplexer> createMultiplexer(const String& id, const int& numLogicInputs, const int& numOutputs,
                                                    const PinMode& sigMode) override {
        auto sigPin     = __pPinFactory->createLogicInputPin(1, sigMode);
        auto enablePin  = __pPinFactory->createLogicInputPin(1, PinMode::DigitalOutput);
        auto inputPins  = __pPinFactory->createLogicInputPinSet(numLogicInputs, PinMode::DigitalOutput);
        auto outputPins = __pPinFactory->createLogicOutputPinSet(numOutputs, sigMode);
        auto policy     = new MultiplexerTranslationPolicy();
        return std::make_shared<Multiplexer>(id, inputPins.release(), outputPins.release(), sigPin.release(),
                                             enablePin.release(), policy);
    }

    std::shared_ptr<IValve> createValve(const String& id, const int& onValue, const int& offValue) override {
        auto inputPin = __pPinFactory->createLogicInputPin(0, PinMode::DigitalOutput);
        return std::make_shared<Valve>(id, inputPin.release(), onValue, offValue);
    }

    std::shared_ptr<IMoistureSensor> createMoistureSensor(const String& id, const float& scaler) override {
        auto inputPin = __pPinFactory->createLogicInputPin(0, PinMode::AnalogInput);
        return std::make_shared<MoistureSensor>(id, inputPin.release(), scaler);
    }

    std::shared_ptr<IPump> createPump(const String& id, const int& onValue, const int& offValue) override {
        auto inputPin = __pPinFactory->createLogicInputPin(0, PinMode::DigitalOutput);
        return std::make_shared<Pump>(id, inputPin.release(), onValue, offValue);
    }

    std::shared_ptr<ILiquidLevelSensor> createLiquidLevelSensor(const String& id, const int& okValue) override {
        auto inputPin = __pPinFactory->createLogicInputPin(0, PinMode::DigitalInput);
        return std::make_shared<LiquidLevelSensor>(id, inputPin.release(), okValue);
    }

private:
    std::unique_ptr<ISignalFactory> __pSignalFactory;
    std::unique_ptr<IPinFactory> __pPinFactory;
};