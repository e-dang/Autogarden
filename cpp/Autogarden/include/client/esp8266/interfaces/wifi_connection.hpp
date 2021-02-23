#pragma once

class IWifiConnection {
public:
    virtual ~IWifiConnection() = default;

    virtual void connect() = 0;

    virtual bool isConnected() = 0;
};