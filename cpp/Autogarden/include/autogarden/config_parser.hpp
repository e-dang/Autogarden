#pragma once

#include <autogarden/duration_parser.hpp>
#include <autogarden/interfaces/config_parser.hpp>

struct WateringStationConfigs {
    uint32_t duration;
    float threshold;
    bool status;
};

class WateringStationConfigParser : public IWateringStationConfigParser<WateringStationConfigs> {
public:
    WateringStationConfigs parse(const JsonObject& configs) override {
        auto duration  = configs["watering_duration"].as<uint32_t>() * 1000;
        auto threshold = configs["moisture_threshold"];
        auto status    = configs["status"];
        return { duration, threshold, status };
    }
};