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
from ..lib import ab_color_attributes, ab_common

class CategoryBaseColorAttributes(ab_common.Category):
    category = "Attributes/Colors"
    category_arg = ab_common.OperatorCategories.CUSTOM
    category_icon = 'GROUP_VCOL'

    @classmethod
    def poll(cls, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        return len(targets)>0 and\
        ab_color_attributes.get_color_attribute_channel_count(targets)

class ABColorAttributeSelection(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty()
    selected : bpy.props.BoolProperty(name = "")

class OpABRemoveVertexColorsFromSelected(bpy.types.Operator, CategoryBaseColorAttributes):
    """Removes all Color Attributes from selected objects"""
    bl_idname = "object.ab_remove_vertex_colors_from_selected"
    bl_label = "Remove all Color Attributes from selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):        
        for obj in bpy.context.selected_objects:
            ab_color_attributes.remove_vertex_colors_from_object(obj)

        return {'FINISHED'}
    
class OpABDeleteColorAttributes(bpy.types.Operator, CategoryBaseColorAttributes):
    """Deletes the marked Color Attribute(s)"""
    bl_idname = "object.ab_delete_color_attributes"
    bl_label = "Delete Color Attribute(s)"
    bl_options = {'REGISTER', 'UNDO'}

    selected_color_attrib : bpy.props.CollectionProperty(
        type = ABColorAttributeSelection
    )

    deselect_invalid : bpy.props.BoolProperty(
        name = "Deselect Invalid",
        default = True
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        for obj in targets:
            try:
                for col in self.selected_color_attrib:
                    target_col : bpy.types.FloatColorAttribute\
                    | bpy.types.ByteColorAttribute = obj.data.color_attributes[col.name]
                    obj.data.color_attributes.remove(target_col)
            except:
                if self.deselect_invalid:
                    obj.select_set(False)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        color_attributes : tuple[str] = ab_color_attributes.get_unique_color_attrib_names_from_selected(targets = targets)
        for col in color_attributes:
            col_attrib = self.selected_color_attrib.add()
            col_attrib.name = col
        return context.window_manager.invoke_props_dialog(self)
        
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text = "Color Attribute Layer Selection")
        box = col.box()
        col.prop(self, "deselect_invalid")
        for col in self.selected_color_attrib:
            row = box.row()
            row.prop(col, 'selected')
            row.label(text = col.name, icon = 'GROUP_VCOL')

class OpABRenameColorAttribute(bpy.types.Operator, CategoryBaseColorAttributes):
    """Renames the selected Color Attribute"""
    bl_idname = "object.ab_rename_color_attribute"
    bl_label = "Rename Color Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    new_name : bpy.props.StringProperty(
        name = "Name",
        default = "Color"
    )

    target_color_attrib : bpy.props.EnumProperty(
        items = ab_color_attributes.unique_color_attribute_list,
        name = "Target Color Attribute"
    )

    deselect_invalid : bpy.props.BoolProperty(
        name = "Deselect Invalid",
        default = True
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        for obj in targets:
            try:
                obj.data.color_attributes.get(self.target_color_attrib).name = self.new_name
            except:
                if self.deselect_invalid:
                    obj.select_set(False)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class OpABSetActiveColorAttribute(bpy.types.Operator, CategoryBaseColorAttributes):
    """Sets the active color attribute on the selected objects.\n
    If the channel does not exist, the active color attribute is not set on the other object"""
    bl_idname = "object.ab_set_active_color_attribute"
    bl_label = "Set active Color Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    target_color_attrib : bpy.props.EnumProperty(
        items = ab_color_attributes.unique_color_attribute_list,
        name = "Target Color Attribute"
    )

    deselect_invalid : bpy.props.BoolProperty(
        name = "Deselect Invalid",
        default = True
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        for obj in targets:
            try:
                obj.data.color_attributes.active_color_name = self.target_color_attrib
            except:
                if self.deselect_invalid:
                    obj.select_set(False)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        
class OpABColorAttributeRenderSet(bpy.types.Operator, CategoryBaseColorAttributes):
    """Sets which color attribute should be rendered"""
    bl_idname = "object.ab_color_attribute_render_set"
    bl_label = "Set Color Attributes to render"
    bl_options = {'REGISTER', 'UNDO'}

    target_color_attrib : bpy.props.EnumProperty(
        items = ab_color_attributes.unique_color_attribute_list,
        name = "Target Color Attribute"
    )

    deselect_invalid : bpy.props.BoolProperty(
        name = "Deselect Invalid",
        default = True
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
        for obj in targets:
            try:
                target_color_idx : int = -1
                for i, col in enumerate(obj.data.color_attributes):
                    if col.name == self.target_color_attrib:
                        target_color_idx = i
                obj.data.color_attributes.render_color_index = target_color_idx
            except:
                if self.deselect_invalid:
                    obj.select_set(False)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
OPERATORS : tuple[bpy.types.Operator] = (OpABColorAttributeRenderSet,
                                         OpABDeleteColorAttributes,
                                         OpABRenameColorAttribute,
                                         OpABRemoveVertexColorsFromSelected,
                                         OpABSetActiveColorAttribute)
PROPERTIES : tuple[bpy.types.PropertyGroup] = (ABColorAttributeSelection,)