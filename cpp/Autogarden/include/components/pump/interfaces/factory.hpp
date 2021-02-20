#pragma once

#include <components/pump/interfaces/pump.hpp>

class IPumpFactory {
public:
    virtual ~IPumpFactory() = default;

    virtual std::unique_ptr<IPump> create(const std::string& id, const int& onValue, const int& offValue) = 0;
};