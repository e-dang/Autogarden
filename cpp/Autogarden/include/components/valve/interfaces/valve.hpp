#pragma once

class IValve {
public:
    virtual ~IValve() = default;

    virtual bool open() = 0;

    virtual bool close() = 0;
};