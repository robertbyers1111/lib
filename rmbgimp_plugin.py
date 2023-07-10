#!/bin/env python
# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
rmbgimp_plugin.py - My GIMP plugin

Place this file in your gimp plug-in directory. No need to run or load this file. As long as it exists in
the plug-ins directory it will be auto-loaded upon gimp startup (e.g., ~/.config/GIMP/2.10/plug-ins)

All operations are currently accessible via the Rmbjr60 menu in GIMP (see 'menu=' lines below for latest location)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from gimpfu import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def center_elements_horizontally(image, drawable):
"""
Centers all visible layers in the horizontal dimension. Vertical position is untouched.
"""
    layers = []
    listAllVisible(image, layers)
    for layer in layers:
        pdb.gimp_layer_set_offsets(
            layer,
            image.width/2 - layer.width/2,
            layer.offsets[1]
        )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def center_elements_vertically(image, drawable):
"""
Centers all visible layers in the vertical dimension. Horizontal position is untouched.
"""
    run_gegl('x.jpg', 'y.jpg')

    layers = []
    listAllVisible(image, layers)
    for layer in layers:
        pdb.gimp_layer_set_offsets(
            layer,
            layer.offsets[0],
            image.height/2 - layer.height/2
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def listAllVisible(parent, outputList):
"""
Updates a list of all currently visible layers.

NOTES:

• This is a potentially recursive function.
• Recursion occurs when a layer is detected to belong to a group.
• outputList is passed by reference and, as such, should be initialized by the caller (!)

"""

    for layer in parent.layers:
        if pdb.gimp_layer_get_visible(layer):
            outputList.append(layer)
            if pdb.gimp_item_is_group(layer):
                listAllVisible(layer, outputList)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ***  M A I N  ***
#
# Registers and runs the plugin
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

register(
    "python-fu-center_elements_horizontally",
    "Center all visible layers",
    "Center all visible layers (in the horizontal dimention only)",
    "rmbjr60", "rmbjr60", "2023",
    "Center Elements Horizontally",
    "",
    [
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
    ],
    [],
    center_elements_horizontally,
    menu="<Image>/Rmbjr60"
)

register(
    "python-fu-center_elements_vertically",
    "Center all visible layers",
    "Center all visible layers (in the horizontal dimention only)",
    "rmbjr60", "rmbjr60", "2023",
    "Center Elements Vertically",
    "",
    [
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
    ],
    [],
    center_elements_vertically,
    menu="<Image>/Rmbjr60"
)

main()

