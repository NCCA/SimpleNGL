# SimpleNGL 

![alt tag](SimpleNGL.png)


This is the most basic version of an NGL demo, it creates a simple window in Qt and allows the manipulation of the teapot using the mouse.

This uses a simple PBR shader based on code from [here](https://learnopengl.com/PBR/Theory) 

## Building

This requires that NGL is installed in $(HOME)/NGL (or other system path) and that the required vcpkg installs are in place.

To build use

```
mkdir build
cd build
cmake -DCMAKE_TOOLCHAIN_FILE=[vcpkg toolchain location] ..
cmake --build .
```

Note under Windows the default project will be placed in your build/Debug folder, also note you need to build against the debug version of NGL (which is also the default)

