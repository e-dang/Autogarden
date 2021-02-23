#include <gtest/gtest.h>

#include <autogarden/autogarden.hpp>
#include <mocks/mock_api_client.hpp>
#include <mocks/mock_microcontroller.hpp>
#include <mocks/mock_watering_station.hpp>

using namespace ::testing;

class AutoGardenTest : public Test {
protected:
    ServerConfigs configs;
    const int numWateringStations = 1;
    const char* uuid              = "random-chars";

    MockAPIClient* mockClient;
    std::vector<NiceMock<MockWateringStation>*> mockWateringStations;
    MockMicroController* mockController;

    std::unique_ptr<MockAPIClient> tmpClient;
    std::vector<std::unique_ptr<IWateringStation>> tmpWateringStations;
    std::unique_ptr<MockMicroController> tmpController;
    std::unique_ptr<AutoGarden> autogarden;

    AutoGardenTest() :
        tmpClient(new MockAPIClient()),
        mockWateringStations(numWateringStations),
        tmpController(new MockMicroController()) {
        configs        = { numWateringStations, uuid };
        mockClient     = tmpClient.get();
        mockController = tmpController.get();
        for (auto& station : mockWateringStations) {
            station = new NiceMock<MockWateringStation>();
            tmpWateringStations.emplace_back(station);
        }

        autogarden = std::make_unique<AutoGarden>(configs, std::move(tmpClient), std::move(tmpWateringStations),
                                                  std::move(tmpController));
    }
};

TEST_F(AutoGardenTest, initializePins) {
    const auto value = true;
    EXPECT_CALL(*mockController, initialize()).WillOnce(Return(value));

    EXPECT_EQ(autogarden->initializePins(), value);
}

TEST_F(AutoGardenTest, initializeServer) {
    EXPECT_CALL(*mockClient, initializeServer(configs.toJson()));

    autogarden->initializeServer();
}

TEST_F(AutoGardenTest, refreshWateringStations) {
    DynamicJsonDocument configs(1024);
    for (int i = 0; i < numWateringStations; i++) {
        JsonObject data;
        configs.add(data);
        ON_CALL(*mockWateringStations[i], getIdx()).WillByDefault(Return(i));
        EXPECT_CALL(*mockWateringStations[i], update(data));
    }
    EXPECT_CALL(*mockClient, fetchConfigs()).WillOnce(Return(configs));

    autogarden->refreshWateringStations();
}

TEST_F(AutoGardenTest, run) {
    for (int i = 0; i < numWateringStations; i++) {
        EXPECT_CALL(*mockWateringStations[i], activate());
    }

    autogarden->run();
}