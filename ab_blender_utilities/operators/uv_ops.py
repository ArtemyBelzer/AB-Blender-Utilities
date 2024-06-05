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
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, StringProperty
from bpy.types import MeshUVLoopLayer, Operator, PropertyGroup

from .categories import CatUV
from ..lib.uv import get_uv_list_from_selected, get_uv_names_from_objects


class ABBU_PT_UV_Selection(PropertyGroup):
    name : StringProperty()
    selected : BoolProperty(name = "")

class ABBU_OT_AddUVLayer(Operator, CatUV):
    """Adds a UV layer to one or more objects"""
    bl_idname = "wm.abbu_ad_uv_layer"
    bl_label = "Add UV Layer"
    bl_options = {'REGISTER', 'UNDO'}

    new_name : StringProperty(
        name = "Name",
        default = "UVMap"
    )

    set_as_active : BoolProperty(
        name = "Set as Active",
        default = False
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                uv = o.data.uv_layers.new(name = self.new_name)
                if self.set_as_active:
                    o.data.uv_layers.active = uv

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class ABBU_OT_DeleteUVLayers(Operator, CatUV):
    """Deletes multiple UV layers from one or more objects.\nAny UV layers that are checked will be deleted"""
    bl_idname = "wm.abbu_delete_uv_layers"
    bl_label = "Delete UV Layer(s)"
    bl_options = {'REGISTER', 'UNDO'}

    uv_layers : CollectionProperty(
        type = ABBU_PT_UV_Selection
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                for uv in self.uv_layers:
                    if uv.name in o.data.uv_layers:
                        if uv.selected:
                            uvl : MeshUVLoopLayer = o.data.uv_layers[uv.name]
                            o.data.uv_layers.remove(uvl)
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.uv_layers.clear()
        uv_names : tuple[str] = get_uv_names_from_objects(bpy.context.selected_objects)
        
        for uv in uv_names:
            uv_c = self.uv_layers.add()
            uv_c.name = uv
        return context.window_manager.invoke_props_dialog(self)
        
    def draw(self, context):
        col = self.layout.column()
        col.label(text = "UV Map Layer Selection")
        box = col.box()
        for uv in self.uv_layers:
            row = box.row()

            row.prop(uv, 'selected')
            row.label(text = uv.name, icon = 'GROUP_UVS')

class ABBU_OT_RenameUVLayer(Operator, CatUV):
    """Renames a UV layer on one or more objects"""
    bl_idname = "wm.abbu_rename_uv_layer"
    bl_label = "Rename UV Layer"
    bl_options = {'REGISTER', 'UNDO'}

    new_name : StringProperty(
        name = "Name",
        default = "UVMap"
    )

    uv : EnumProperty(
        items = get_uv_list_from_selected,
        name = "Target UV Layer"
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                if self.uv in o.data.uv_layers:
                    target_uv : MeshUVLoopLayer = o.data.uv_layers[self.uv]
                    target_uv.name = self.new_name

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class ABBU_OT_SetActiveUV(Operator, CatUV):
    """Sets the active UV layer on one or more objects"""
    bl_idname = "wm.abbu_set_active_uv"
    bl_label = "Set Active UV Layer"
    bl_options = {'REGISTER', 'UNDO'}

    uv : EnumProperty(
        items = get_uv_list_from_selected,
        name = "Target UV Layer"
    )

    deselect_invalid : BoolProperty(
        name = "Deselect Invalid",
        default = True
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                if self.uv in o.data.uv_layers:
                    uv : MeshUVLoopLayer = o.data.uv_layers[self.uv]
                    o.data.uv_layers.active = uv
                else:
                    if self.deselect_invalid:
                        o.select_set(False)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

OPERATORS : tuple[Operator] = (ABBU_OT_AddUVLayer,
                               ABBU_OT_DeleteUVLayers,
                               ABBU_OT_SetActiveUV,
                               ABBU_OT_RenameUVLayer)

PROPERTIES : tuple[PropertyGroup] = (ABBU_PT_UV_Selection,)
