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
from bpy.types import Panel

from . import constants
from .persistent import get_preferences

_preferences = None

class ABBU_PT_Panel(Panel):
    bl_idname = "ABBU_PT_Panel"
    bl_label = "Panel"
    bl_category = constants.plugin_name_short
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    operators = []
    panel_show_var = None

    @classmethod
    def poll(cl, context) -> bool:
        return getattr(_preferences, cl.panel_show_var)

    def draw(self : any, context: any) -> None:
        layout = self.layout
        categories = dict()
        for op in self.operators:
            if op.category == self.bl_label:
                layout.operator(op.bl_idname)
                continue
            if op.category not in categories:
                categories.update({op.category : layout.box()})
                categories[op.category].label(text = op.category_split[0], icon = op.category_icon)
            categories[op.category].operator(op.bl_idname)

class ABBU_PT_Cleanup(ABBU_PT_Panel):
    bl_idname = "ABBU_PT_Cleanup"
    bl_label = "Cleanup"
    panel_show_var = "show_cleanup_panel"
    operators = []

class ABBU_PT_Data(ABBU_PT_Panel):
    bl_idname = "ABBU_PT_Data"
    bl_label = "Data"
    panel_show_var = "show_data_panel"
    operators = []

class ABBU_PT_File(ABBU_PT_Panel):
    bl_idname = "ABBU_PT_File"
    bl_label = "File"
    panel_show_var = "show_file_panel"
    operators = []

class ABBU_PT_Modifiers(ABBU_PT_Panel):
    bl_idname = "ABBU_PT_Modifiers"
    bl_label = "Modifiers"
    panel_show_var = "show_modifiers_panel"
    operators = []

class ABBU_PT_Naming(ABBU_PT_Panel):
    bl_idname = "ABBU_PT_Naming"
    bl_label = "Naming"
    panel_show_var = "show_naming_panel"
    operators = []

class ABBU_PT_Objects(ABBU_PT_Panel):
    bl_idname = "ABBU_PT_Objects"
    bl_label = "Objects"
    panel_show_var = "show_object_panel"
    operators = []

class ABBU_PT_Selection(ABBU_PT_Panel):
    bl_idname = "ABBU_PT_Selection"
    bl_label = "Selection"
    panel_show_var = "show_selection_panel"
    operators = []

class ABBU_PT_UVs(ABBU_PT_Panel):
    bl_idname = "ABBU_PT_UVs"
    bl_label = "UVs"
    panel_show_var = "show_uv_panel"
    operators = []

__panels : tuple = {ABBU_PT_Cleanup.bl_label : ABBU_PT_Cleanup,
                    ABBU_PT_Data.bl_label : ABBU_PT_Data,
                    ABBU_PT_File.bl_label : ABBU_PT_File,
                    ABBU_PT_Modifiers.bl_label : ABBU_PT_Modifiers,
                    ABBU_PT_Naming.bl_label : ABBU_PT_Naming,
                    ABBU_PT_Objects.bl_label : ABBU_PT_Objects,
                    ABBU_PT_Selection.bl_label : ABBU_PT_Selection,
                    ABBU_PT_UVs.bl_label : ABBU_PT_UVs}

__panel_registration_order = []

def __assign_classes(classes : tuple) -> None:
    for cl in classes:
        cl_categories = cl.category.split("/")
        panel_category = cl_categories[0]
        __panels[panel_category].operators.append(cl)

def load(classes : list) -> None:
    global _preferences, __panel_registration_order
    __panel_registration_order.clear()

    _preferences = get_preferences()

    for key, panel in __panels.items():
        bpy.utils.register_class(panel)
        __panel_registration_order.append(panel)

    __assign_classes(classes)

def unload() -> None:
    for panel in reversed(__panel_registration_order):
        bpy.utils.unregister_class(panel)
        panel.operators.clear()
