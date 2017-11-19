#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibtiffConan(ConanFile):
    name = "libtiff"
    description = "Library for Tag Image File Format (TIFF)"
    version = "4.0.8"
    url = "http://github.com/bincrafters/conan-tiff"
    license = "https://spdx.org/licenses/libtiff.html"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = "zlib/1.2.11@conan/stable"
    generators = "cmake"
    exports = ["CMakeLists.txt", "FindTIFF.cmake"]

    def source(self):
        zip_name = "tiff-" + self.version + ".zip"
        tools.get("http://download.osgeo.org/libtiff/" + zip_name)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["lzma"] = False
        cmake.definitions["jpeg"] = False
        if self.options.shared and self.settings.compiler == "Visual Studio":
            # https://github.com/Microsoft/vcpkg/blob/master/ports/tiff/fix-cxx-shared-libs.patch
            tools.replace_in_file(os.path.join('tiff-4.0.8', 'libtiff', 'CMakeLists.txt'),
                                  r'set_target_properties(tiffxx PROPERTIES SOVERSION ${SO_COMPATVERSION})',
                                  r'set_target_properties(tiffxx PROPERTIES SOVERSION ${SO_COMPATVERSION} '
                                  r'WINDOWS_EXPORT_ALL_SYMBOLS ON)')
        if self.settings.os == "Linux":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(build_dir="build")
        cmake.build(target="install")

    def package(self):
        self.copy("*.h", dst="include", src="sources")

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["tiffd", "tiffxxd"]
        else:
            self.cpp_info.libs = ["tiff", "tiffxx"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
