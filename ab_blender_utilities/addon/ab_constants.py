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

from typing import Final

# General
plugin_name_short : Final[str] = "AB Utilities"
plugin_menu_name : Final[str] = "Extra Utilities"
plugin_name_internal : Final[str] = 'ab_utility'

# Errors
info : Final[str] = "[AB Extra Utilities]: "
error : Final[str] = "[AB Extra Utilities Error]: "
warning : Final[str] = "[AB Extra Utilities Warning]: "

# Baking
bake_suffixes : Final[tuple[str]] = ("_high", "_low", "_High", "_Low")

# Data blocks
block_types : Final[tuple[str]] = ("meshes", "materials", "textures", "images")

# Preference tabs
e_pref_tab : Final[tuple[tuple]] = (('GENERAL', "General", ""),
                                   ('NAMING', "Naming", ""),
                                   ('KEYS', "Keybindings", ""),
                                   ('QUICK_EXPORT', "Quick Export", ""),
                                   ('ADVANCED', "Advanced", ""))

# Selection
e_selection : Final[tuple[tuple]] = (('SELECTED', "Selected", ""),
                                     ('ALL', "All", ""))

# String find action
e_string_find_action : Final[tuple[tuple]] = (('CONTAINS', "Contains", ""),
                                              ('BEGINS_WITH', "Begins with", ""),
                                              ('ENDS_WITH', "Ends with", ""))

# Add/Remove enum
e_add_remove : Final[tuple[tuple]] = (('ADD', "Add", ""),
                                      ('REMOVE', "Remove", ""))

# Preference tabs
e_pref_display_tab : Final[tuple[tuple]] = (('SUBMENUS', "Menus", ""),
                                           ('PANELS', "Panels", ""),
                                           ('SUBMENU_BUTTONS', "Button Menus", ""),
                                           ('PANELS_IN_PROPERTIES', "Property Panel", ""))

# Missing Conditions
missing_condition_msg : Final[str] = "The conditions to use these operators were not met. Please read the descriptions or the \"ReadMe\" of the addon."
missing_condition_msg_panel : Final[str] = "The conditions to use these operators were not met."

# Menu init error
menus_not_initialized : Final[str] = "Menus are not initialzied."
menus_initialized : Final[str] = "Menus are already initialzied."

panels_not_initialized : Final[str] = "Panels are not initialzied."
panels_initialized : Final[str] = "Panels are already initialzied."

# Input class errors
input_classes_none : Final[str] = "The input classes are missing. (NoneType)"

# Prefs
prefs_keymap_do_not_remove_msg : Final[str] = "Please do not remove the keymaps."
prefs_keymap_disable_msg : Final[str] = "Disable them instead by unchecking the box on the left."

restore_selection_description : Final[str] = "Restores the selection before quick exporting.\nIf unchecked, the current selection will be the final export object and its children."
export_wired_description : Final[str] = "Export objects that have the 'Wired' display type."