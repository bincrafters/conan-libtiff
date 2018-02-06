#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class LibtiffConan(ConanFile):
    name = "libtiff"
    description = "Library for Tag Image File Format (TIFF)"
    version = "4.0.8"
    url = "http://github.com/bincrafters/conan-tiff"
    license = "BSD"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "FindTIFF.cmake"]
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    requires = "zlib/[~=1.2]@conan/stable"

    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        tools.get("http://download.osgeo.org/libtiff/tiff-{0}.zip".format(self.version))
        os.rename('tiff-' + self.version, self.source_subfolder)
        os.rename(os.path.join(self.source_subfolder, "CMakeLists.txt"),
                  os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"))
        shutil.copy("CMakeLists.txt",
                    os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["lzma"] = False
        cmake.definitions["jpeg"] = False
        if self.options.shared and self.settings.compiler == "Visual Studio":
            # https://github.com/Microsoft/vcpkg/blob/master/ports/tiff/fix-cxx-shared-libs.patch
            tools.replace_in_file(os.path.join(self.source_subfolder, 'libtiff', 'CMakeLists.txt'),
                                  r'set_target_properties(tiffxx PROPERTIES SOVERSION ${SO_COMPATVERSION})',
                                  r'set_target_properties(tiffxx PROPERTIES SOVERSION ${SO_COMPATVERSION} '
                                  r'WINDOWS_EXPORT_ALL_SYMBOLS ON)')

        if self.settings.os == "Windows" and self.settings.compiler != "Visual Studio":
            # only one occurence must be patched
            tools.replace_in_file(os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"),
                                  "if (UNIX)",
                                  "if (UNIX OR MINGW)")

        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindTIFF.cmake", ".", ".")
        shutil.rmtree(os.path.join(self.package_folder, 'share'), ignore_errors=True)

    def package_info(self):
        self.cpp_info.libs = ["tiff", "tiffxx"]
        if self.settings.os == "Windows" and self.settings.build_type == "Debug" and self.settings.compiler == 'Visual Studio':
            self.cpp_info.libs = [lib+'d' for lib in self.cpp_info.libs]
        if self.options.shared and self.settings.os == "Windows" and self.settings.compiler != 'Visual Studio':
            self.cpp_info.libs = [lib+'.dll' for lib in self.cpp_info.libs]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
        self.output.warn(repr(self.cpp_info.libs))
