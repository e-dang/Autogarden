template <typename T>
T* ptr(T& obj) {
    return &obj;
}

template <typename T>
T* ptr(T* obj) {
    return obj;
}