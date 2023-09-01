# Artemy Belzer's Blender Utilities - Additional Blender utilities.
# Copyright (C) 2023 Artemy Belzer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from types import ModuleType
from . import ab_keymaps, ab_persistent, ab_op_menus, ab_prefs, ab_constants, ab_op_panels
from .. import operators


__classes : any = []
__properties : any = []
__exporters : ExportHelper = []
__importers : ImportHelper = []
__preferences : any = None

def reload():
    return []

def register():
    global __classes, __exporters, __importers, __preferences

    # Addon preference class
    bpy.utils.register_class(ab_prefs.PanelVars)
    bpy.utils.register_class(ab_prefs.ABUtilAddonPrefs)
    __preferences = bpy.props.PointerProperty(type=ab_prefs.ABUtilAddonPrefs)

    # Append Operators from imported Modules into a list of __classes.
    dynamic_modules : ModuleType = operators.get_modules()

    for module in dynamic_modules:
        if hasattr(module, "PROPERTIES"):  # Find EXPORTERS in modules
            for prop in module.PROPERTIES:
                __properties.append(prop)
        for cls in module.OPERATORS:
            __classes.append(cls)
        if hasattr(module, "EXPORTERS"):  # Find EXPORTERS in modules
            for cls in module.EXPORTERS:
                __exporters.append(cls)
        if hasattr(module, "IMPORTERS"):  # Find EXPORTERS in modules
            for cls in module.IMPORTERS:
                __importers.append(cls)

    # Property Registration
    for prop in __properties:
        try:
            bpy.utils.register_class(prop)
        except Exception as e:
                print(f"{ab_constants.error}{e}")

    # Add menu list into global class list
    __classes += ab_op_menus.load(__classes)

    if ab_persistent.get_preferences().load_viewport_panel:
        __classes += ab_op_panels.load(__classes)

    for cls in __classes:
            try:
                bpy.utils.register_class(cls)
            except Exception as e:
                print(f"{ab_constants.error}{e}")

    # Adds __exporters and __importers to the file_export menu
    for cls in __exporters:
        bpy.types.TOPBAR_MT_file_export.append(cls.menu_func)
    for cls in __importers:
        bpy.types.TOPBAR_MT_file_import.append(cls.menu_func)

    # Register keymaps
    if not ab_persistent.get_preferences().do_not_load_keymaps:
        ab_keymaps.register(__classes)

    # Load settings
    ab_persistent.load()

def unregister():
    global __classes, __exporters, __importers, __preferences
    ab_op_menus.unload()
    
    # Removes __exporters and __importers from the file_export menu
    for cls in __exporters:
        bpy.types.TOPBAR_MT_file_export.remove(cls.menu_func)
    for cls in __importers:
        bpy.types.TOPBAR_MT_file_import.remove(cls.menu_func)

    for cls in __classes:
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"{ab_constants.error}{e}\n\
                  Class = {cls}")
            
    # Property de-registration
    for prop in __properties:
        try:
            bpy.utils.unregister_class(prop)
        except Exception as e:
                print(f"{ab_constants.error}{e}")
    
    # Unload any persistent info
    ab_persistent.unload()

    # Unregister keymaps
    ab_keymaps.unregister()

    # Addon preference class
    bpy.utils.unregister_class(ab_prefs.ABUtilAddonPrefs)
    bpy.utils.unregister_class(ab_prefs.PanelVars)

    __classes = []
    __exporters = []
    __importers = []
    __preferences = None
    