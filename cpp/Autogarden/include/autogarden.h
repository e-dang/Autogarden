#define ARDUINOJSON_USE_LONG_LONG 1

#ifdef ARDUINO  // clang-format off

#include <memory> // clang-format off
namespace std
{
template <typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}
}  // namespace std

#endif

#include <autogarden/factory.hpp>
#include <client/api_client.hpp>
#include <components/components.hpp>