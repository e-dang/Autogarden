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
    const bool status       = true;
    const uint32_t duration = 600000;
    const float threshold   = 50.f;
    std::shared_ptr<NiceMock<MockMoistureSensor>> mockSensor;
    std::shared_ptr<NiceMock<MockPump>> mockPump;
    std::shared_ptr<NiceMock<MockValve>> mockValve;
    std::shared_ptr<NiceMock<MockWateringStationConfigParser>> mockParser;
    std::unique_ptr<WateringStation> station;

    void SetUp() {
        mockSensor = std::make_shared<NiceMock<MockMoistureSensor>>();
        mockPump   = std::make_shared<NiceMock<MockPump>>();
        mockValve  = std::make_shared<NiceMock<MockValve>>();
        mockParser = std::make_shared<NiceMock<MockWateringStationConfigParser>>();
        station = std::make_unique<WateringStation>(idx, status, duration, threshold, mockPump, mockValve, mockSensor,
                                                    mockParser);
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

TEST_F(WateringStationTest, activate_performs_routine_when_reading_is_below_threshold_and_isActive_returns_true) {
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

TEST_F(WateringStationTest, activate_doesnt_perform_routine_when_reading_is_above_threshold_and_isActive_returns_true) {
    MockArduino mockArduino;
    setMockArduino(&mockArduino);

    const float reading = threshold + 1.;
    EXPECT_CALL(*mockSensor, readScaled()).WillOnce(Return(reading));
    EXPECT_CALL(*mockValve, open()).Times(0);
    EXPECT_CALL(*mockValve, close()).Times(0);
    EXPECT_CALL(*mockPump, start()).Times(0);
    EXPECT_CALL(*mockPump, stop()).Times(0);
    EXPECT_CALL(mockArduino, _delay(duration)).Times(0);

    station->activate();

    setMockArduino(nullptr);
}

TEST_F(WateringStationTest,
       activate_doesnt_perform_routine_when_reading_is_below_threshold_and_isActive_returns_false) {
    MockArduino mockArduino;
    setMockArduino(&mockArduino);
    station->setStatus(false);

    const float reading = threshold - 1.;
    EXPECT_CALL(*mockSensor, readScaled()).WillOnce(Return(reading));
    EXPECT_CALL(*mockValve, open()).Times(0);
    EXPECT_CALL(*mockValve, close()).Times(0);
    EXPECT_CALL(*mockPump, start()).Times(0);
    EXPECT_CALL(*mockPump, stop()).Times(0);
    EXPECT_CALL(mockArduino, _delay(duration)).Times(0);

    station->activate();

    setMockArduino(nullptr);
}

TEST_F(WateringStationTest, isActive_returns_status_true) {
    station->setStatus(true);

    EXPECT_TRUE(station->isActive());
}

TEST_F(WateringStationTest, isActive_returns_status_false) {
    station->setStatus(false);

    EXPECT_FALSE(station->isActive());
}

TEST_F(WateringStationTest, getData_returns_json_object_containing_data_read_during_call_to_activate) {
    NiceMock<MockArduino> mockArduino;
    setMockArduino(&mockArduino);
    const float reading = threshold - 2.3;
    ON_CALL(*mockSensor, readScaled()).WillByDefault(Return(reading));
    station->activate();

    auto retVal = station->getData();

    EXPECT_FLOAT_EQ(retVal["moisture_level"], reading);

    setMockArduino(nullptr);
}

INSTANTIATE_TEST_SUITE_P(WateringStationTest, ParametrizedWateringStationTest,
                         Values(std::tuple<float, bool>{ -1., false }, std::tuple<float, bool>{ 101., false }));