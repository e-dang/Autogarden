#pragma once

#include <autogarden/config_parser.hpp>
#include <autogarden/interfaces/watering_station.hpp>
#include <components/components.hpp>

class WateringStation : public IWateringStation {
public:
    WateringStation(const int& idx, const uint32_t& duration, const float& threshold, std::shared_ptr<IPump> pump,
                    std::shared_ptr<IValve> valve, std::shared_ptr<IMoistureSensor> sensor,
                    std::shared_ptr<IWateringStationConfigParser<WateringStationConfigs>> parser) :
        __mIdx(idx),
        __mDuration(duration),
        __mThreshold(threshold),
        __pPump(pump),
        __pValve(valve),
        __pSensor(sensor),
        __pParser(parser) {}

    void activate() override {
        if (__pSensor->readScaled() < __mThreshold) {
            __pValve->open();
            __pPump->start();
            delay(__mDuration);
            __pPump->stop();
            __pValve->close();
        }
    }

    bool update(const DynamicJsonDocument& configs) override {
        auto parsedConfigs = __pParser->parse(configs);
        if (setThreshold(parsedConfigs.threshold)) {
            setDuration(parsedConfigs.duration);
            return true;
        }
        return false;
    }

    void setDuration(const uint32_t& duration) {
        __mDuration = duration;
    }

    bool setThreshold(const float& threshold) {
        if (threshold < 0. || threshold > 100.)
            return false;

        __mThreshold = threshold;
        return true;
    }

    int getIdx() const override {
        return __mIdx;
    }

    uint32_t getDuration() const {
        return __mDuration;
    }

    int getThreshold() const {
        return __mThreshold;
    }

private:
    int __mIdx;
    uint32_t __mDuration;
    float __mThreshold;
    std::shared_ptr<IPump> __pPump;
    std::shared_ptr<IValve> __pValve;
    std::shared_ptr<IMoistureSensor> __pSensor;
    std::shared_ptr<IWateringStationConfigParser<WateringStationConfigs>> __pParser;
};
