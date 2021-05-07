#pragma once

#include <autogarden/autogarden.hpp>
#include <autogarden/interfaces/factory.hpp>
#include <autogarden/watering_station.hpp>

struct AutoGardenConfigs {
    String microControllerId;
    std::initializer_list<int> digitalOutput;
    std::initializer_list<int> digitalInput;
    std::initializer_list<int> analogOutput;
    std::initializer_list<int> analogInput;

    String shiftRegisterId;
    int shiftRegisterNumOutputPins;
    int shiftRegisterDirection;

    String dMuxId;
    int dMuxNumInputPins;
    int dMuxNumOutputPins;
    PinMode dMuxPinMode;

    String aMuxId;
    int aMuxNumInputPins;
    int aMuxNumOutputPins;
    PinMode aMuxPinMode;

    String pumpId;
    int pumpOnValue;
    int pumpOffValue;

    String sensorId;
    float sensorScaler;

    String valveId;
    int valveOnValue;
    int valveOffValue;

    String liquidLevelSensorId;
    int okValue;

    String apiKey;
    String gardenName;
    int numWateringStations;

    String ssid;
    String password;
    String rootUrl;
};

class AutoGardenFactory : public IAutoGardenFactory {
public:
    AutoGardenFactory(AutoGardenConfigs* configs, std::unique_ptr<IComponentFactory>&& componentFactory,
                      std::unique_ptr<IAPIClientFactory>&& clientFactory) :
        __pConfigs(configs),
        __pComponentFactory(std::move(componentFactory)),
        __pClientFactory(std::move(clientFactory)) {}

    std::unique_ptr<IAutoGarden> create() override {
        auto client     = __pClientFactory->create(__pConfigs->gardenName, __pConfigs->apiKey, __pConfigs->ssid,
                                               __pConfigs->password, __pConfigs->rootUrl);
        auto controller = __pComponentFactory->createMicroController(
          __pConfigs->microControllerId, __pConfigs->digitalOutput, __pConfigs->digitalInput, __pConfigs->analogOutput,
          __pConfigs->analogInput);
        auto liquidLevelSensor =
          __pComponentFactory->createLiquidLevelSensor(__pConfigs->liquidLevelSensorId, __pConfigs->okValue);
        auto wateringStations = _createWateringStations(controller.get());
        controller->appendChild(liquidLevelSensor);

        return std::make_unique<AutoGarden>(std::move(client), std::move(wateringStations), std::move(controller),
                                            liquidLevelSensor);
    }

private:
    std::vector<std::unique_ptr<IWateringStation>> _createWateringStations(Component* controller) {
        std::vector<std::unique_ptr<IWateringStation>> wateringStations;

        auto shiftRegister = __pComponentFactory->createShiftRegister(
          __pConfigs->shiftRegisterId, __pConfigs->shiftRegisterNumOutputPins, __pConfigs->shiftRegisterDirection);
        auto dMux = __pComponentFactory->createMultiplexer(__pConfigs->dMuxId, __pConfigs->dMuxNumInputPins,
                                                           __pConfigs->dMuxNumOutputPins, __pConfigs->dMuxPinMode);
        auto aMux = __pComponentFactory->createMultiplexer(__pConfigs->aMuxId, __pConfigs->aMuxNumInputPins,
                                                           __pConfigs->aMuxNumOutputPins, __pConfigs->aMuxPinMode);
        auto pump =
          __pComponentFactory->createPump(__pConfigs->pumpId, __pConfigs->pumpOnValue, __pConfigs->pumpOffValue);

        controller->appendChild(shiftRegister);
        controller->appendChild(pump);
        shiftRegister->appendChild(dMux);
        shiftRegister->appendChild(aMux);

        auto configParser = std::make_shared<WateringStationConfigParser>();
        for (int i = 0; i < __pConfigs->numWateringStations; i++) {
            auto sensor =
              __pComponentFactory->createMoistureSensor(__pConfigs->sensorId + String(i), __pConfigs->sensorScaler);
            auto valve = __pComponentFactory->createValve(__pConfigs->valveId + String(i), __pConfigs->valveOnValue,
                                                          __pConfigs->valveOffValue);

            dMux->appendChild(valve);
            aMux->appendChild(sensor);
            wateringStations.emplace_back(
              std::make_unique<WateringStation>(i, true, 0, 0, pump, valve, sensor, configParser));
        }

        return wateringStations;
    }

private:
    AutoGardenConfigs* __pConfigs;
    std::unique_ptr<IComponentFactory> __pComponentFactory;
    std::unique_ptr<IAPIClientFactory> __pClientFactory;
};

struct SimpleAutoGardenConfigs {
    String microControllerId;
    std::initializer_list<int> digitalOutput;
    std::initializer_list<int> digitalInput;
    std::initializer_list<int> analogOutput;
    std::initializer_list<int> analogInput;

    String pumpId;
    int pumpOnValue;
    int pumpOffValue;

    String apiKey;
    String gardenName;

    String ssid;
    String password;
    String rootUrl;
};

class SimpleAutoGardenFactory : public IAutoGardenFactory {
public:
    SimpleAutoGardenFactory(SimpleAutoGardenConfigs* configs, std::unique_ptr<IComponentFactory>&& componentFactory,
                            std::unique_ptr<IAPIClientFactory>&& clientFactory) :
        __pConfigs(configs),
        __pComponentFactory(std::move(componentFactory)),
        __pClientFactory(std::move(clientFactory)) {}

    std::unique_ptr<IAutoGarden> create() override {
        auto client     = __pClientFactory->create(__pConfigs->gardenName, __pConfigs->apiKey, __pConfigs->ssid,
                                               __pConfigs->password, __pConfigs->rootUrl);
        auto controller = __pComponentFactory->createMicroController(
          __pConfigs->microControllerId, __pConfigs->digitalOutput, __pConfigs->digitalInput, __pConfigs->analogOutput,
          __pConfigs->analogInput);
        auto wateringStations = _createWateringStations(controller.get());

        return std::make_unique<SimpleAutoGarden>(std::move(client), std::move(wateringStations),
                                                  std::move(controller));
    }

private:
    std::vector<std::unique_ptr<IWateringStation>> _createWateringStations(Component* controller) {
        std::vector<std::unique_ptr<IWateringStation>> wateringStations;

        auto pump =
          __pComponentFactory->createPump(__pConfigs->pumpId, __pConfigs->pumpOnValue, __pConfigs->pumpOffValue);

        controller->appendChild(pump);

        auto configParser = std::make_shared<WateringStationConfigParser>();
        wateringStations.emplace_back(std::make_unique<SimpleWateringStation>(0, true, 0, pump, configParser));

        return wateringStations;
    }

private:
    SimpleAutoGardenConfigs* __pConfigs;
    std::unique_ptr<IComponentFactory> __pComponentFactory;
    std::unique_ptr<IAPIClientFactory> __pClientFactory;
};