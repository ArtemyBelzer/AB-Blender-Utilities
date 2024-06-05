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
from bpy.types import AddonPreferences, KeyConfig, KeyMap, KeyMapItem, WindowManager

from . import persistent

__loaded_keymaps : list = []


def name_prop_exists_in_kmi(kmi : KeyMapItem) -> bool:
    if hasattr(kmi.properties, "name"):
        return True
    return False

def copy_keymap(in_kmi : KeyMapItem,
                out_km : KeyMap) -> KeyMapItem:
    """Copies a `KeyMapItem` into a target `KeyMap`.\n
    Returns the new `KeyMapItem`."""
    out_kmi : KeyMapItem
    if name_prop_exists_in_kmi(in_kmi):
        out_kmi = out_km.keymap_items.new_from_item(in_kmi)
        out_kmi.properties.name = in_kmi.properties.name
    else:
        out_kmi = out_km.keymap_items.new_from_item(in_kmi)
    return out_kmi

def get_user_keymaps() -> list[tuple[KeyMap, KeyMapItem]]:
    """Returns a `list` of `tuples` containing a `KeyMap` and a `KeyMapItem` into the user layer based on the addon layer."""
    prefs : AddonPreferences = persistent.get_preferences()
    user_keymaps : list = []
    wm : WindowManager = bpy.context.window_manager
    kc : KeyConfig = wm.keyconfigs.user  # User key configs
    km_user : KeyMap = kc.keymaps["Window"]

    for km_addon, kmi_addon, in __loaded_keymaps:
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

def register() -> None:
    # Load keymaps from file

    wm : WindowManager = bpy.context.window_manager
    kc : KeyConfig = wm.keyconfigs.addon  # Addon key configs
    km : KeyMap
    if "window" in kc.keymaps:
        km = kc.keymaps["Window"]
    else:
        km = kc.keymaps.new(name="Window")

    km_auto_rename : KeyMapItem = km.keymap_items.new(idname = "wm.abbu_custom_expression_object_rename",
                                                    type = 'F2',
                                                    value = 'PRESS',
                                                    ctrl = False,
                                                    alt = True,
                                                    shift = False)
    __loaded_keymaps.append((km, km_auto_rename))

    kmi_qe : KeyMapItem = km.keymap_items.new(idname = "wm.call_menu_pie",
                                type = 'E',
                                value = 'PRESS',
                                ctrl = False,
                                alt = True,
                                shift = False)
    kmi_qe.properties.name = "AABU_MT_Utility_Menu_Pie"
    __loaded_keymaps.append((km, kmi_qe))

def unregister() -> None:
    for km, kmi in __loaded_keymaps:
        km.keymap_items.remove(kmi)
    __loaded_keymaps.clear()
