import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class LibtiffConan(ConanFile):
    name = "libtiff"
    description = """Library for Tag Image File Format (TIFF), a widely used
                     format for storing image data"""
    version = "4.0.8"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = "zlib/1.2.11@conan/stable"
    exports = ["CMakeLists.txt", "FindTIFF.cmake"]
    url="http://github.com/ZaMaZaN4iK/conan-tiff"
    license="http://www.remotesensing.org/libtiff/"

    def source(self):
        zip_name = "tiff-%s.zip" % self.version
        download("http://download.osgeo.org/libtiff/%s" % zip_name , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["lzma"] = "OFF"
        cmake.definitions["jpeg"] = "OFF"
        if self.settings.os == "Linux":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        if self.options.shared == False:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        cmake.configure(build_dir="build")
        cmake.build(target="install")

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["tiffd", "tiffxxd"]
        else:
            self.cpp_info.libs = ["tiff", "tiffxx"]
