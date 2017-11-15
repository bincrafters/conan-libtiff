#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools


class LibtiffConan(ConanFile):
    name = "libtiff"
    description = "Library for Tag Image File Format (TIFF)"
    version = "4.0.8"
    url="http://github.com/bincrafters/conan-tiff"
    license="https://spdx.org/licenses/libtiff.html"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = "zlib/1.2.11@lasote/stable"
    generators = "cmake"
    exports = ["CMakeLists.txt", "FindTIFF.cmake"]

    def source(self):
        zip_name = "tiff-" + self.version + ".zip"
        tools.get("http://download.osgeo.org/libtiff/" + zip_name)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["lzma"] = "OFF"
        cmake.definitions["jpeg"] = "OFF"
        if self.settings.os == "Linux":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(build_dir="build")
        cmake.build(target="install")
        
    def package(self):
        self.copy("*.h", dst="include", src="sources")

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            self.copy(pattern="libjpeg.lib", dst="lib", src="Release", keep_path=False)
        else:
            self.copy(pattern="*.so", dst="lib", src="libs", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="libs", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["tiffd", "tiffxxd"]
        else:
            self.cpp_info.libs = ["tiff", "tiffxx"]
