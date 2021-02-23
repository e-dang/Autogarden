#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <autogarden/watering_station.hpp>
#include <mocks/mock_arduino.hpp>
#include <mocks/mock_moisture_sensor.hpp>
#include <mocks/mock_pump.hpp>
#include <mocks/mock_valve.hpp>
#include <mocks/mock_watering_station_config_parser.hpp>

using namespace ::testing;

class WateringStationTest : public Test {
protected:
    const int idx           = 0;
    const uint32_t duration = 600000;
    const float threshold   = 50.f;
    std::shared_ptr<MockMoistureSensor> mockSensor;
    std::shared_ptr<MockPump> mockPump;
    std::shared_ptr<MockValve> mockValve;
    std::shared_ptr<MockWateringStationConfigParser> mockParser;
    std::unique_ptr<WateringStation> station;

    void SetUp() {
        mockSensor = std::make_shared<MockMoistureSensor>();
        mockPump   = std::make_shared<MockPump>();
        mockValve  = std::make_shared<MockValve>();
        mockParser = std::make_shared<MockWateringStationConfigParser>();
        station =
          std::make_unique<WateringStation>(idx, duration, threshold, mockPump, mockValve, mockSensor, mockParser);
    }
};

class ParametrizedWateringStationTest :
    public WateringStationTest,
    public WithParamInterface<std::tuple<float, bool>> {};

TEST_F(WateringStationTest, getIdx) {
    EXPECT_EQ(station->getIdx(), idx);
}

TEST_F(WateringStationTest, getDuration) {
    EXPECT_EQ(station->getDuration(), duration);
}

TEST_F(WateringStationTest, getThreshold) {
    EXPECT_FLOAT_EQ(station->getThreshold(), threshold);
}

TEST_F(WateringStationTest, setDuration) {
    const uint32_t newDuration = duration + 1;

    station->setDuration(newDuration);

    EXPECT_EQ(station->getDuration(), newDuration);
}

TEST_P(ParametrizedWateringStationTest, setThreshold_return_false) {
    auto newThreshold   = std::get<0>(GetParam());
    auto expectedRetVal = std::get<1>(GetParam());

    auto retVal = station->setThreshold(newThreshold);

    EXPECT_EQ(retVal, expectedRetVal);
    EXPECT_FLOAT_EQ(station->getThreshold(), threshold);
}

TEST_F(WateringStationTest, setThreshold_return_true) {
    float newThreshold = 89.;

    auto retVal = station->setThreshold(newThreshold);

    EXPECT_TRUE(retVal);
    EXPECT_FLOAT_EQ(station->getThreshold(), newThreshold);
}

TEST_F(WateringStationTest, update_returns_true) {
    const uint32_t newDuration = duration + 10;
    const float newThreshold   = threshold + 1.;
    JsonObject configs;
    WateringStationConfigs parsedConfigs = { newDuration, newThreshold };

    EXPECT_CALL(*mockParser, parse(configs)).WillOnce(Return(parsedConfigs));

    EXPECT_TRUE(station->update(configs));
    EXPECT_EQ(station->getDuration(), newDuration);
    EXPECT_FLOAT_EQ(station->getThreshold(), newThreshold);
}

TEST_F(WateringStationTest, update_returns_false) {
    const uint32_t newDuration = duration + 10;
    const float newThreshold   = 101.;
    JsonObject configs;
    WateringStationConfigs parsedConfigs = { newDuration, newThreshold };

    EXPECT_CALL(*mockParser, parse(configs)).WillOnce(Return(parsedConfigs));

    EXPECT_FALSE(station->update(configs));
    EXPECT_EQ(station->getDuration(), duration);
    EXPECT_FLOAT_EQ(station->getThreshold(), threshold);
}

TEST_F(WateringStationTest, activate_when_reading_is_below_threshold) {
    MockArduino mockArduino;
    setMockArduino(&mockArduino);

    const float reading = threshold - 1.;
    EXPECT_CALL(*mockSensor, readScaled()).WillOnce(Return(reading));
    EXPECT_CALL(*mockValve, open());
    EXPECT_CALL(*mockValve, close());
    EXPECT_CALL(*mockPump, start());
    EXPECT_CALL(*mockPump, stop());
    EXPECT_CALL(mockArduino, _delay(duration));

    station->activate();

    setMockArduino(nullptr);
}

INSTANTIATE_TEST_SUITE_P(WateringStationTest, ParametrizedWateringStationTest,
                         Values(std::tuple<float, bool>{ -1., false }, std::tuple<float, bool>{ 101., false }));