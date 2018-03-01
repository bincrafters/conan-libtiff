#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import platform

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=True)

    items = []
    for item in builder.items:
        # skip mingw cross-builds
        if not (platform.system() == "Windows" and item.settings["compiler"] == "gcc" and
                item.settings["arch"] == "x86"):
            items.append(item)
    builder.items = items

    builder.run()
