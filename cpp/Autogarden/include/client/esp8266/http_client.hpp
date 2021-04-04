#pragma once

#include <ESP8266HTTPClient.h>

#include <client/esp8266/wifi_connection.hpp>
#include <client/interfaces/http_client.hpp>

class ESP8266HttpClient : public IHttpClient {
public:
    ESP8266HttpClient(std::unique_ptr<IWifiConnection>&& connection) : _pConnection(std::move(connection)) {}

    HttpResponse get(const HttpRequest& request) override {
        HttpResponse response;
        if (request.method != "get") {
            response.processingError = true;
            return response;
        }

        _connect();

        _preprocess(request);
        response.statusCode = _mClient.GET();
        _postprocess(response);

        return response;
    }

    HttpResponse post(const HttpRequest& request) override {
        HttpResponse response;
        if (request.method != "post") {
            response.processingError = true;
            return response;
        }

        _connect();

        _preprocess(request);
        response.statusCode = _mClient.POST(request.toString());
        _postprocess(response);

        return response;
    }

    HttpResponse patch(const HttpRequest& request) override {
        HttpResponse response;
        if (request.method != "patch") {
            response.processingError = true;
            return response;
        }

        _connect();

        _preprocess(request);
        response.statusCode = _mClient.PATCH(request.toString());
        _postprocess(response);

        return response;
    }

    int getConnectionStrength() const {
        return _pConnection->getConnectionStrength();
    }

protected:
    void _connect() {
        if (!_pConnection->isConnected())
            _pConnection->connect();
    }

    virtual void _preprocess(const HttpRequest& request) {
        _mClient.begin(request.url);
        _mClient.addHeader("Content-Type", request.contentType);
        _mClient.addHeader("Authorization", "Token " + request.authorization);
    }

    void _postprocess(HttpResponse& response) {
        response.data            = _mClient.getString();
        response.processingError = false;
        _mClient.end();
    }

protected:
    HTTPClient _mClient;
    std::unique_ptr<IWifiConnection> _pConnection;
};

class ESP8266HttpClientFactory : public IHttpClientFactory {
public:
    std::unique_ptr<IHttpClient> create(const String& ssid, const String& password,
                                        const int& waitTime = 1000) override {
        std::unique_ptr<IWifiConnection> connection = std::make_unique<WifiConnection>(ssid, password, waitTime);
        return std::make_unique<ESP8266HttpClient>(std::move(connection));
    }
};