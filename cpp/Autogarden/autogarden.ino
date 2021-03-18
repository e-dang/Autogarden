#include <autogarden.h>

AutoGardenConfigs configs = {
    "controller",
    { D2, D3, D4, D8, D9, D5, D6 },
    { D11 },
    {},
    { A0 },
    "reg",
    8,
    MSBFIRST,
    "dMux",
    4,
    16,
    PinMode::DigitalOutput,
    "aMux",
    4,
    16,
    PinMode::AnalogInput,
    "pump",
    HIGH,
    LOW,
    "sensor",
    0.,
    "valve",
    HIGH,
    LOW,
    "llSensor",
    HIGH,
    "",  // apiKey
    "",  // ssid
    "",  // wifi password
    ""   // domain name of server
};

std::unique_ptr<IAutoGarden> autogarden;

std::unique_ptr<IAutoGarden> createAutoGarden() {
    auto componentFactory =
      std::make_unique<ComponentFactory>(std::make_unique<SignalFactory>(), std::make_unique<PinFactory>());
    auto clientFactory = std::make_unique<APIClientFactory>(std::make_unique<ESP8266HttpClientFactory>());
    AutoGardenFactory factory(&configs, std::move(componentFactory), std::move(clientFactory));
    return factory.create();
}

void setup() {
    Serial.begin(9600);
    autogarden = createAutoGarden();
    autogarden->initialize();
}

void loop() {
    autogarden->run();
}