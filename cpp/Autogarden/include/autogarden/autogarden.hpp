#pragma once

#include <autogarden/interfaces/autogarden.hpp>
#include <autogarden/interfaces/watering_station.hpp>
#include <client/interfaces/api_client.hpp>
#include <components/components.hpp>

struct ServerConfigs {
    int numWateringStations;
    const char* uuid;

    DynamicJsonDocument toJson() const {
        DynamicJsonDocument doc(1024);
        doc["uuid"]                = uuid;
        doc["numWateringStations"] = numWateringStations;
        doc.shrinkToFit();
        return doc;
    }
};

class AutoGarden : public IAutoGarden {
public:
    AutoGarden(const ServerConfigs& configs, std::unique_ptr<IAPIClient>&& client,
               std::vector<std::unique_ptr<IWateringStation>>&& wateringStations,
               std::unique_ptr<IMicroController>&& controller) :
        __mServerConfigs(configs),
        __pClient(std::move(client)),
        __mWateringStations(std::move(wateringStations)),
        __pMicroController(std::move(controller)) {}

    bool initializePins() override {
        return __pMicroController->initialize();
    }

    void initializeServer() override {
        __pClient->initializeServer(__mServerConfigs.toJson());
    }

    void refreshWateringStations() override {
        auto configs = __pClient->fetchConfigs();
        __updateWateringStations(configs.as<JsonArray>());
    }

    void run() override {
        for (auto& station : __mWateringStations) {
            station->activate();
        }
    }

private:
    void __updateWateringStations(const JsonArray& configs) {
        for (auto& station : __mWateringStations) {
            station->update(configs[station->getIdx()].as<JsonObject>());
        }
    }

private:
    ServerConfigs __mServerConfigs;
    std::unique_ptr<IAPIClient> __pClient;
    std::unique_ptr<IMicroController> __pMicroController;
    std::vector<std::unique_ptr<IWateringStation>> __mWateringStations;
};