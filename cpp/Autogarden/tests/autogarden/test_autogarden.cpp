#include <gtest/gtest.h>

#include <autogarden/autogarden.hpp>
#include <mocks/mock_api_client.hpp>
#include <mocks/mock_liquid_level_sensor.hpp>
#include <mocks/mock_microcontroller.hpp>
#include <mocks/mock_watering_station.hpp>
#include <string>

using namespace ::testing;

class AutoGardenTest : public Test {
protected:
    const int numWateringStations = 1;

    MockAPIClient* mockClient;
    std::vector<NiceMock<MockWateringStation>*> mockWateringStations;
    MockMicroController* mockController;
    MockLiquidLevelSensor* mockLLSensor;

    std::unique_ptr<MockAPIClient> tmpClient;
    std::vector<std::unique_ptr<IWateringStation>> tmpWateringStations;
    std::unique_ptr<MockMicroController> tmpController;
    std::unique_ptr<MockLiquidLevelSensor> tmpLLSensor;
    std::unique_ptr<AutoGarden> autogarden;

    AutoGardenTest() :
        tmpClient(new MockAPIClient()),
        mockWateringStations(numWateringStations),
        tmpController(new MockMicroController()),
        tmpLLSensor(new MockLiquidLevelSensor()) {
        mockClient     = tmpClient.get();
        mockController = tmpController.get();
        mockLLSensor   = tmpLLSensor.get();
        for (auto& station : mockWateringStations) {
            station = new NiceMock<MockWateringStation>();
            tmpWateringStations.emplace_back(station);
        }

        autogarden = std::make_unique<AutoGarden>(std::move(tmpClient), std::move(tmpWateringStations),
                                                  std::move(tmpController), std::move(tmpLLSensor));
    }
};

TEST_F(AutoGardenTest, initialize) {
    const auto value = true;
    EXPECT_CALL(*mockController, initialize()).WillOnce(Return(value));

    EXPECT_EQ(autogarden->initialize(), value);
}

TEST_F(AutoGardenTest, updateWateringStationConfigs_calls_update_on_configs_returned_from_client) {
    DynamicJsonDocument configs(1024);
    for (int i = 0; i < numWateringStations; i++) {
        JsonObject data;
        configs.add(data);
        ON_CALL(*mockWateringStations[i], getIdx()).WillByDefault(Return(i));
        EXPECT_CALL(*mockWateringStations[i], update(data));
    }
    EXPECT_CALL(*mockClient, getWateringStationConfigs()).WillOnce(Return(configs));

    autogarden->updateWateringStationConfigs();
}

TEST_F(AutoGardenTest, updateGardenConfigs_sets_update_frequency_on_autogarden_instance) {
    uint64_t updateFrequency = 239867;
    DynamicJsonDocument configs(1024);
    configs["update_frequency"] = std::to_string(updateFrequency);
    EXPECT_CALL(*mockClient, getGardenConfigs()).WillOnce(Return(configs));

    autogarden->updateGardenConfigs();

    EXPECT_EQ(autogarden->getUpdateFrequency(), updateFrequency);
}

TEST_F(AutoGardenTest, activateWateringStations_calls_activate_on_each_watering_station) {
    for (int i = 0; i < numWateringStations; i++) {
        EXPECT_CALL(*mockWateringStations[i], activate());
    }

    autogarden->activateWateringStations();
}

TEST_F(AutoGardenTest, sendGardenData_calls_sendGardenData_on_client_with_garden_data) {
    DynamicJsonDocument data(1024);
    int connectionStrength      = -23;
    const char* waterLevel      = "lo";
    data["water_level"]         = waterLevel;
    data["connection_strength"] = connectionStrength;
    EXPECT_CALL(*mockLLSensor, read()).WillOnce(Return(waterLevel));
    EXPECT_CALL(*mockClient, getConnectionStrength()).WillOnce(Return(connectionStrength));
    EXPECT_CALL(*mockClient, sendGardenData(data));

    autogarden->sendGardenData();
}

TEST_F(AutoGardenTest, sendWateringStationData_calls_sendWateringStationData_on_client_with_watering_station_data) {
    DynamicJsonDocument data(1024);
    for (auto& station : mockWateringStations) {
        JsonObjectConst wsData;
        data.add(wsData);
        EXPECT_CALL(*station, getData()).WillOnce(Return(wsData));
    }
    EXPECT_CALL(*mockClient, sendWateringStationData(data));

    autogarden->sendWateringStationData();
}