#include <gmock/gmock.h>

#include <components/multiplexer/interfaces/translation_policy.hpp>

class MockMultiplexerTranslationPolicy : public IMultiplexerTranslationPolicy {
public:
    MOCK_METHOD(bool, translate,
                (ILogicInputPinSet * inputPins, ILogicOutputPinSet* outputPins, ILogicInputPin* sigPin), (override));
};