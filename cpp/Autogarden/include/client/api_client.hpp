#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>

#include <client/esp8266/http_client.hpp>
#include <client/interfaces/api_client.hpp>
#include <client/interfaces/http_client.hpp>

class APIClient : public IAPIClient {
public:
    APIClient(const String& rootUrl, std::unique_ptr<IHttpClient>&& client,
              const String& contentType = "application/json") :
        __mPK(""), __mRootUrl(rootUrl), __mContentType(contentType), __pClient(std::move(client)) {}

    void initializeServer(const DynamicJsonDocument& data) override {
        HttpRequest request;
        request.url         = getInitializationUrl();
        request.method      = "post";
        request.contentType = __mContentType;
        request.data        = data;

        while (String(__mPK.toInt()) != __mPK) {
            auto response = __pClient->post(request);
            if (response.statusCode > 0)
                __setPk(response.getJsonData());
        }
    }

    DynamicJsonDocument fetchConfigs() override {
        HttpRequest request;
        request.url         = getWateringStationsUrl();
        request.method      = "get";
        request.contentType = __mContentType;

        HttpResponse response;
        while (true) {
            response = __pClient->get(request);
            if (response.statusCode > 0)
                break;
        }

        return response.getJsonData();
    }

    String getWateringStationsUrl() const override {
        auto url = getInitializationUrl() + "<?>/watering-stations/";
        url.replace("<?>", __mPK);
        return url;
    }

    String getInitializationUrl() const override {
        return __mRootUrl + "api/garden/";
    }

private:
    void __setPk(const DynamicJsonDocument& data) {
        __mPK = data["pk"].as<String>();
    }

private:
    String __mPK;
    String __mRootUrl;
    String __mContentType;
    std::unique_ptr<IHttpClient> __pClient;
};

class APIClientFactory : public IAPIClientFactory {
public:
    APIClientFactory(std::unique_ptr<IHttpClientFactory>&& httpClientFactory) :
        __pHttpClientFactory(std::move(httpClientFactory)) {}

    std::unique_ptr<IAPIClient> create(const String& ssid, const String& password, const String& rootUrl,
                                       const int& waitTime = 1000) override {
        auto httpClient = __pHttpClientFactory->create(ssid, password, waitTime);
        return std::make_unique<APIClient>(rootUrl, std::move(httpClient));
    }

private:
    std::unique_ptr<IHttpClientFactory> __pHttpClientFactory;
};