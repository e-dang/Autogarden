Commands to setup:
```
export VCPKG_ROOT=<root dir of vcpkg install>
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
cd build && make
```