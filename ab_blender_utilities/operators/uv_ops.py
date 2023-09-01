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
from ..lib import ab_common, ab_uv

class CategoryBaseUVs(ab_common.Category):
    category = "UVs"
    category_arg = ab_common.OperatorCategories.CUSTOM
    category_icon = 'UV'

    @classmethod
    def poll(cls, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        return len(targets)>0 and\
        ab_uv.get_uv_channel_count(targets)

class ABUVSelection(bpy.types.PropertyGroup):
    uv_channel : bpy.props.StringProperty()
    uv_selected : bpy.props.BoolProperty(name = "")

class OpABAddUVChannel(bpy.types.Operator, CategoryBaseUVs):
    """Adds UV channels on selected objects"""
    bl_idname = "object.ab_add_uv_channel_on_selected"
    bl_label = "Add UV Channel"
    bl_options = {'REGISTER', 'UNDO'}

    category_arg = ab_common.OperatorCategories.SELECTION

    new_name : bpy.props.StringProperty(
        name = "Name",
        default = "UVMap"
    )

    set_as_active : bpy.props.BoolProperty(
        name = "Set as Active",
        default = False
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        for obj in targets:
            try:
                obj.data.uv_layers.new(name = self.new_name)
                if self.set_as_active:
                    obj.data.uv_layers.active = obj.data.uv_layers[self.new_name]
            except Exception as e:
                ab_common.error(self, e)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class OpABSetActiveUVChannel(bpy.types.Operator, CategoryBaseUVs):
    """Sets the active UV channel on the selected objects.\n
    If the channel does not exist, the active UV channel is not set on the other object"""
    bl_idname = "object.ab_set_active_uv_channel"
    bl_label = "Set active UV Channel"
    bl_options = {'REGISTER', 'UNDO'}

    target_uv_channel : bpy.props.EnumProperty(
        items = ab_uv.unique_uv_channel_list,
        name = "Target UV Channel"
    )

    deselect_invalid : bpy.props.BoolProperty(
        name = "Deselect Invalid",
        default = True
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        for obj in targets:
            try:
                target_uv : bpy.types.MeshUVLoopLayer = obj.data.uv_layers[self.target_uv_channel]
                obj.data.uv_layers.active = target_uv
            except:
                if self.deselect_invalid:
                    obj.select_set(False)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        
class OpABRenameUVChannel(bpy.types.Operator, CategoryBaseUVs):
    """Sets the active UV channel on the selected objects.\n
    If the channel does not exist, the active UV channel is not set on the other object"""
    bl_idname = "object.ab_rename_uv_channel"
    bl_label = "Rename UV Channel"
    bl_options = {'REGISTER', 'UNDO'}

    new_name : bpy.props.StringProperty(
        name = "Name",
        default = "UVMap"
    )

    target_uv_channel : bpy.props.EnumProperty(
        items = ab_uv.unique_uv_channel_list,
        name = "Target UV Channel"
    )

    deselect_invalid : bpy.props.BoolProperty(
        name = "Deselect Invalid",
        default = True
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        for obj in targets:
            try:
                target_uv : bpy.types.MeshUVLoopLayer = obj.data.uv_layers[self.target_uv_channel]
                target_uv.name = self.new_name
            except:
                if self.deselect_invalid:
                    obj.select_set(False)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class OpABDeleteUVChannel(bpy.types.Operator, CategoryBaseUVs):
    """Deletes the marked UV channels"""
    bl_idname = "object.ab_delete_uv_channel"
    bl_label = "Delete UV Channel(s)"
    bl_options = {'REGISTER', 'UNDO'}

    selected_uv_channels : bpy.props.CollectionProperty(
        type = ABUVSelection
    )

    deselect_invalid : bpy.props.BoolProperty(
        name = "Deselect Invalid",
        default = True
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        for obj in targets:
            try:
                for uv in self.selected_uv_channels:
                    target_uv : bpy.types.MeshUVLoopLayer = obj.data.uv_layers[uv.uv_channel]
                    obj.data.uv_layers.remove(target_uv)
            except:
                if self.deselect_invalid:
                    obj.select_set(False)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        uv_channels : tuple[str] = ab_uv.get_unique_uv_channel_names_from_selected(targets = targets)
        for uv in uv_channels:
            uv_channel = self.selected_uv_channels.add()
            uv_channel.uv_channel = uv
        return context.window_manager.invoke_props_dialog(self)
        
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text = "UV Map Layer Selection")
        box = col.box()
        for uv in self.selected_uv_channels:
            row = box.row()
            # row.label(text = uv, icon = 'GROUP_UVS')
            row.prop(uv, 'uv_selected')
            row.label(text = uv.uv_channel, icon = 'GROUP_UVS')
        col.prop(self, "deselect_invalid")
    
OPERATORS : tuple[bpy.types.Operator] = (OpABAddUVChannel,
                                         OpABSetActiveUVChannel,
                                         OpABRenameUVChannel,
                                         OpABDeleteUVChannel)
PROPERTIES : tuple[bpy.types.PropertyGroup] = (ABUVSelection,)
