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
from . import ab_persistent

__loaded_keymaps__ : list = []


def name_prop_exists_in_kmi(kmi : bpy.types.KeyMapItem) -> bool:
    if hasattr(kmi.properties, "name"):
        return True
    return False

def copy_keymap(in_kmi : bpy.types.KeyMapItem,
                out_km : bpy.types.KeyMap) -> bpy.types.KeyMapItem:
    """Copies a `KeyMapItem` into a target `KeyMap`.\n
    Returns the new `KeyMapItem`."""
    out_kmi : bpy.types.KeyMapItem
    if name_prop_exists_in_kmi(in_kmi):
        out_kmi = out_km.keymap_items.new_from_item(in_kmi)
        out_kmi.properties.name = in_kmi.properties.name
    else:
        out_kmi = out_km.keymap_items.new_from_item(in_kmi)
    return out_kmi

def get_user_keymaps() -> list[tuple[bpy.types.KeyMap, bpy.types.KeyMapItem]]:
    """Returns a `list` of `tuples` containing a `KeyMap` and a `KeyMapItem` into the user layer based on the addon layer."""
    prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()
    user_keymaps : list = []
    wm : bpy.types.WindowManager = bpy.context.window_manager
    kc : bpy.types.KeyConfig = wm.keyconfigs.user  # User key configs
    km_user : bpy.types.KeyMap = kc.keymaps["Window"]

    for km_addon, kmi_addon, in __loaded_keymaps__:
        has_name_prop : bool = name_prop_exists_in_kmi(kmi_addon)
        keymap_found : bool = False
        if has_name_prop:
            for kmi_user in km_user.keymap_items:
                if kmi_user.idname == kmi_addon.idname\
                and kmi_user.properties.name == kmi_addon.properties.name:
                    user_keymaps.append((km_user, kmi_user))
                    keymap_found = True
                    break
            if not keymap_found and prefs.auto_re_add_missing_keymaps:
                copy_keymap(kmi_addon, km_user)
        else:
            user_keymaps.append((km_user, km_user.keymap_items.get(kmi_addon.idname)))
            if km_user.keymap_items.get(kmi_addon.idname) is not None:
                keymap_found = True
            if not keymap_found and prefs.auto_re_add_missing_keymaps:
                copy_keymap(kmi_addon, km_user)

    return user_keymaps

def register(classes : tuple | list = ()) -> None:
    # Load keymaps from file

    wm : bpy.types.WindowManager = bpy.context.window_manager
    kc : bpy.types.KeyConfig = wm.keyconfigs.addon  # Addon key configs
    km : bpy.types.KeyMap
    if "window" in kc.keymaps:
        km = kc.keymaps["Window"]
    else:
        km = kc.keymaps.new(name="Window")

    km_auto_rename : bpy.types.KeyMapItem = km.keymap_items.new(idname = "wm.ab_auto_rename",
                                                    type = 'F2',
                                                    value = 'PRESS',
                                                    ctrl = False,
                                                    alt = True,
                                                    shift = False)
    __loaded_keymaps__.append((km, km_auto_rename))

    kmi_qe : bpy.types.KeyMapItem = km.keymap_items.new(idname = "wm.call_menu_pie",
                                type = 'E',
                                value = 'PRESS',
                                ctrl = False,
                                alt = True,
                                shift = False)
    kmi_qe.properties.name = "OBJECT_MT_ab_utility_base_menu_pie"
    __loaded_keymaps__.append((km, kmi_qe))

    kmi_qe : bpy.types.KeyMapItem = km.keymap_items.new(idname = "wm.call_menu",
                                type = 'E',
                                value = 'PRESS',
                                ctrl = False,
                                alt = False,
                                shift = True)
    kmi_qe.properties.name = "OBJECT_MT_ab_utility_base_menu"
    # kmi_qe.active = False
    __loaded_keymaps__.append((km, kmi_qe))

    kmi_name_pie : bpy.types.KeyMapItem = km.keymap_items.new("wm.call_menu_pie",
                                                                    type = "F2",
                                                                    value = "PRESS",
                                                                    ctrl = False,
                                                                    alt = True,
                                                                    shift = True)
    kmi_name_pie.properties.name = "OBJECT_MT_ab_utility_submenu_naming_pie"
    __loaded_keymaps__.append((km, kmi_name_pie))

def unregister(classes : tuple | list = ()) -> None:
    for km, kmi in __loaded_keymaps__:
        km.keymap_items.remove(kmi)
    __loaded_keymaps__.clear()
