#pragma once

#include <autogarden/interfaces/autogarden.hpp>
#include <autogarden/interfaces/watering_station.hpp>
#include <client/interfaces/api_client.hpp>
#include <components/components.hpp>

class AutoGarden : public IAutoGarden {
public:
    AutoGarden(std::unique_ptr<IAPIClient>&& client, std::vector<std::unique_ptr<IWateringStation>>&& wateringStations,
               std::unique_ptr<IMicroController>&& controller, std::shared_ptr<ILiquidLevelSensor> liquidLevelSensor) :
        __pClient(std::move(client)),
        __mWateringStations(std::move(wateringStations)),
        __pMicroController(std::move(controller)),
        __pLiquidLevelSensor(liquidLevelSensor) {}

    bool initialize() override {
        return __pMicroController->initialize();
    }

    void run() override {
        updateGardenConfigs();
        updateWateringStationConfigs();

        activateWateringStations();

        sendGardenData();
        sendWateringStationData();

        delay(__mUpdateFrequency);
    }

    void updateWateringStationConfigs() {
        auto configs = __pClient->getWateringStationConfigs();
        for (auto& station : __mWateringStations) {
            station->update(configs[station->getIdx()].as<JsonObject>());
        }
    }

    void updateGardenConfigs() {
        auto configs       = __pClient->getGardenConfigs();
        __mUpdateFrequency = configs["update_frequency"].as<uint64_t>();
    }

    void activateWateringStations() {
        for (auto& station : __mWateringStations) {
            station->activate();
        }
    }

    void sendGardenData() {
        auto data = __getGardenData();
        __pClient->sendGardenData(data);
    }

    void sendWateringStationData() {
        auto data = __getWateringStationData();
        __pClient->sendWateringStationData(data);
    }

    uint64_t getUpdateFrequency() const {
        return __mUpdateFrequency;
    }

private:
    DynamicJsonDocument __getGardenData() {
        DynamicJsonDocument data(1024);
        data["water_level"]         = __pLiquidLevelSensor->read();
        data["connection_strength"] = __pClient->getConnectionStrength();
        data.shrinkToFit();
        return data;
    }

    DynamicJsonDocument __getWateringStationData() {
        DynamicJsonDocument data(1024);
        for (auto& station : __mWateringStations) {
            data.add(station->getData());
        }
        data.shrinkToFit();
        return data;
    }

private:
    uint64_t __mUpdateFrequency;
    std::shared_ptr<ILiquidLevelSensor> __pLiquidLevelSensor;
    std::unique_ptr<IAPIClient> __pClient;
    std::unique_ptr<IMicroController> __pMicroController;
    std::vector<std::unique_ptr<IWateringStation>> __mWateringStations;
};