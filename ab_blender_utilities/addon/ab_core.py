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
import traceback
import sys
from bpy_extras.io_utils import ImportHelper, ExportHelper
from types import ModuleType
from typing import Final
from . import ab_constants, ab_debug, ab_keymaps, ab_op_menus, ab_op_panels, ab_persistent, ab_prefs
from .. import operators


__classes : list[bpy.types.Operator | bpy.types.Menu | bpy.types.Panel] = []  # This variable stores operators, menus, and panel types.
__exporters : list[ExportHelper] = []
__importers : list[ImportHelper] = []
__preferences : list[bpy.props.PointerProperty] = []
__properties : list[bpy.types.PropertyGroup] = []

__preference_classes : Final[tuple[bpy.types.AddonPreferences|
                             bpy.types.PropertyGroup|
                             bpy.types.UIList]] = (ab_prefs.PanelVars,
                                                  ab_prefs.ABUTIL_UL_name_slots,
                                                  ab_prefs.ABUtilQuickExportNames,
                                                  ab_prefs.ABUtilAddonPrefs)


def __clear_vars() -> None:
    """Clear variables that store pointers to references to classes."""
    global __classes, __exporters, __importers, __preferences, __properties
    __classes = []
    __exporters = []
    __importers = []
    __preferences = []
    __properties = []

def register():
    global __classes, __exporters, __importers, __preferences, __properties
    __clear_vars()
    
    # Addon preference class
    try:
        for pref_cls in __preference_classes:
            bpy.utils.register_class(pref_cls)
    except Exception as e:
            print(f"{ab_constants.error} Error registering preferences {e}")
    
    __preferences = bpy.props.PointerProperty(type=ab_prefs.ABUtilAddonPrefs)

    # Append Operators from imported Modules into a list of __classes.
    dynamic_modules : ModuleType = operators.get_modules()

    for module in dynamic_modules:
        if hasattr(module, "PROPERTIES")\
            and not ab_debug.skip_loading_properties:  # Find EXPORTERS in modules
            for prop in module.PROPERTIES:
                __properties.append(prop)
        if hasattr(module, "OPERATORS")\
            and not ab_debug.skip_loading_operators:
            for cls in module.OPERATORS:
                __classes.append(cls)
        if hasattr(module, "EXPORTERS")\
            and not ab_debug.skip_loading_exporters:  # Find EXPORTERS in modules
            for cls in module.EXPORTERS:
                __exporters.append(cls)
        if hasattr(module, "IMPORTERS")\
            and not ab_debug.skip_loading_importers:  # Find EXPORTERS in modules
            for cls in module.IMPORTERS:
                __importers.append(cls)

    # Property Registration
    for prop in __properties:
        try:
            bpy.utils.register_class(prop)
        except Exception as e:
            print(f"{ab_constants.error} Error loading properties {e}")

    # Add menu list into global class list
    __classes += ab_op_menus.load(__classes)

    if ab_persistent.get_preferences().load_viewport_panel:
        try:
            __classes += ab_op_panels.load(__classes)
        except Exception as e:
            print(f"{ab_constants.error} Error loading panels {e}")


    for cls in __classes:
            try:
                bpy.utils.register_class(cls)
            except Exception as e:
                print(f"{ab_constants.error} Error registering classes {e}")

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
    global __classes, __exporters, __importers, __preferences, __properties
    ab_op_menus.unload()
    ab_op_panels.unload()
    
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
    
    # Unload any persistent info
    ab_persistent.unload()

    # Unregister keymaps
    ab_keymaps.unregister()

    # Property de-registration
    for prop in __properties:
        bpy.utils.unregister_class(prop)

    # Addon preference class
    try:
        for pref_cls in __preference_classes:
            bpy.utils.unregister_class(pref_cls)
    except Exception as e:
            print(f"{ab_constants.error} Error unregistering preferences {e}")

    __clear_vars()
    