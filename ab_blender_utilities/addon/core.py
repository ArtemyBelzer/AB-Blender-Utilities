# Artemy Belzer's Blender Utilities - Additional Blender utilities.
# Copyright (C) 2023-2024 Artemy Belzer
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
from bpy.props import PointerProperty
from bpy.types import AddonPreferences, PropertyGroup, UIList

from types import ModuleType
from typing import Final
from . import keymaps, op_menus, op_panels, prefs
from .. import operators
from .persistent import get_preferences


__operators = []
__classes_categorized = []
__exporters = []
__importers = []
__preferences = None
__properties = []

__pref_classes : Final[tuple[AddonPreferences | PropertyGroup | UIList]] = (prefs.ABBU_PT_PrefTabs,
                                                                            prefs.ABUTIL_UL_name_slots,
                                                                            prefs.ABBU_PT_Quick_Export,
                                                                            prefs.ABBU_AddonPreferences)


def __clear_vars() -> None:
    """Clear variables that store pointers to references to classes."""
    __operators.clear()
    __classes_categorized.clear()
    __exporters.clear()
    __importers.clear()
    __properties.clear()

def init_props_and_classes(modules : tuple[ModuleType]):
    for module in modules:
        if hasattr(module, "PROPERTIES"):
            for prop in module.PROPERTIES:
                    __properties.append(prop)
        if hasattr(module, "OPERATORS"):
            for cl in module.OPERATORS:
                    __operators.append(cl)
                    if hasattr(cl, "category"):
                        cl.category_split = cl.category.split("/")[1:]
                        __classes_categorized.append(cl)
        if hasattr(module, "EXPORTERS"):
            for cl in module.EXPORTERS:
                    __exporters.append(cl)
        if hasattr(module, "IMPORTERS"):
            for cl in module.IMPORTERS:
                    __importers.append(cl)

    __classes_categorized.sort(key = lambda x : (x.category, x.bl_label))

def register():
    global __preferences

    for pref_cls in __pref_classes:
        bpy.utils.register_class(pref_cls)

    __preferences = PointerProperty(type=prefs.ABBU_AddonPreferences)

    op_modules : tuple[ModuleType] = operators.get_modules()

    init_props_and_classes(op_modules)

    for prop in __properties:
        bpy.utils.register_class(prop)

    # Load menus and panels
    op_menus.load(__classes_categorized)
    op_panels.load(__classes_categorized)

    for op in __operators:
        bpy.utils.register_class(op)

    # Adds __exporters and __importers to the file_export menu
    for cl in __exporters:
        bpy.types.TOPBAR_MT_file_export.append(cl.menu_func)
    for cl in __importers:
        bpy.types.TOPBAR_MT_file_import.append(cl.menu_func)

    # Register keymaps
    if not get_preferences().do_not_load_keymaps:
        keymaps.register()

def unregister():
    # Unregister keymaps
    keymaps.unregister()

    # Removes __exporters and __importers from the file_export menu
    for importer in reversed(__importers):
        bpy.types.TOPBAR_MT_file_import.remove(importer.menu_func)
    for exporter in reversed(__exporters):
        bpy.types.TOPBAR_MT_file_export.remove(exporter.menu_func)

    for op in reversed(__operators):
        bpy.utils.unregister_class(op)

    op_panels.unload()
    op_menus.unload()

    # Property de-registration
    for prop in __properties:
        bpy.utils.unregister_class(prop)

    # Addon preference class
    for pref_cls in reversed(__pref_classes):
        bpy.utils.unregister_class(pref_cls)

    __clear_vars()
