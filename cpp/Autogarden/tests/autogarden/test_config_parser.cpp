#include <gtest/gtest.h>

#include <autogarden/config_parser.hpp>
#include <mocks/mock_duration_parser.hpp>

using namespace ::testing;

TEST(WateringStationConfigParserTest, parse) {
    const uint32_t duration = 60000;
    const float threshold   = 50.;
    DynamicJsonDocument doc(1024);
    doc["watering_duration"]  = duration;
    doc["moisture_threshold"] = threshold;
    auto mockDurationParser   = std::make_unique<MockDurationParser>();
    EXPECT_CALL(*mockDurationParser, getMilliSeconds()).WillOnce(Return(duration));
    WateringStationConfigParser parser(std::move(mockDurationParser));

    auto configs = parser.parse(doc);

    EXPECT_EQ(configs.duration, duration);
    EXPECT_FLOAT_EQ(configs.threshold, threshold);
}
