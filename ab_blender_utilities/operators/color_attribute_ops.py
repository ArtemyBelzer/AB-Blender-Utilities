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
from bpy.types import Operator, PropertyGroup

from .categories import CatColorAttrib, PollType
from ..addon.constants import e_vtx_col_domain, e_vtx_col_data_type
from ..lib.color_attributes import get_unique_color_attrib_names_from_selected, unique_color_attribute_list


class ABBU_PT_Color_Attrib_Selection(PropertyGroup):
    name : StringProperty()
    selected : BoolProperty(name = "")

class ABBU_OT_AddColorAttrib(Operator, CatColorAttrib):
    """Adds a color attribute to one or more selected objects"""
    bl_idname = "object.abbu_add_color_attrib"
    bl_label = "Add Color Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    category_poll = PollType.OBJ_MESH_SEL

    name : StringProperty(
        name = "Name",
        default = "Color"
    )
    
    domain : EnumProperty(
        name = "Domain",
        items = e_vtx_col_domain,
        default = 'POINT'
    )

    data_type : EnumProperty(
        name = "Data Type",
        items = e_vtx_col_data_type,
        default = 'FLOAT_COLOR'
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                o.data.color_attributes.new(name = self.name, domain = self.domain, type = self.data_type)

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "name")
        row = col.row()
        row.prop(self, "domain")
        row = col.row()
        row.prop(self, "data_type")

class ABBU_OT_DeleteColorAttribs(Operator, CatColorAttrib):
    """Deletes the specified color attribute(s) from one or more selected objects"""
    bl_idname = "object.abbu_delete_color_attribs"
    bl_label = "Delete Color Attribute(s)"
    bl_options = {'REGISTER', 'UNDO'}

    selected_color_attrib : CollectionProperty(
        type = ABBU_PT_Color_Attrib_Selection
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                for col in self.selected_color_attrib:
                    if col.name in o.data.color_attributes and col.selected:
                        o.data.color_attributes.remove(o.data.color_attributes[col.name])

        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.selected_color_attrib.clear()
        col_attribs : tuple[str] = get_unique_color_attrib_names_from_selected(targets = bpy.context.selected_objects)
        for col in col_attribs:
            col_attrib = self.selected_color_attrib.add()
            col_attrib.name = col
        return context.window_manager.invoke_props_dialog(self)
        
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text = "Color Attribute Layer Selection")
        box = col.box()
        for col in self.selected_color_attrib:
            row = box.row()
            row.prop(col, 'selected')
            row.label(text = col.name, icon = 'GROUP_VCOL')

class ABBU_OT_RenameColorAttribs(Operator, CatColorAttrib):
    """Renames the selected color attribute on one or more selected objects"""
    bl_idname = "object.abbu_rename_color_attribs"
    bl_label = "Rename Color Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    new_name : StringProperty(
        name = "Name",
        default = "Color"
    )

    target_color_attrib : EnumProperty(
        items = unique_color_attribute_list,
        name = "Target Color Attribute"
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = bpy.context.selected_objects
        for o in targets:
            if self.target_color_attrib in o.data.color_attributes:
                o.data.color_attributes.get(self.target_color_attrib).name = self.new_name

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class ABBU_OT_SetActiveColorAttrib(Operator, CatColorAttrib):
    """Sets the active color attribute on one or more selected objects"""
    bl_idname = "object.abbu_set_active_color_attrib"
    bl_label = "Set Active Color Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    target_color_attrib : EnumProperty(
        items = unique_color_attribute_list,
        name = "Target Color Attribute"
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = bpy.context.selected_objects
        for o in targets:
            if self.target_color_attrib in o.data.color_attributes:
                o.data.color_attributes.active_color_name = self.target_color_attrib

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        
class ABBU_OT_SetRenderColorAttrib(Operator, CatColorAttrib):
    """Specifies which color attribute should be rendered"""
    bl_idname = "object.abbu_set_render_color_attrib"
    bl_label = "Set Color Attributes To Render"
    bl_options = {'REGISTER', 'UNDO'}

    target_color_attrib : EnumProperty(
        items = unique_color_attribute_list,
        name = "Target Color Attribute"
    )

    def execute(self, context):
        targets : tuple[bpy.types.Object] = bpy.context.selected_objects
        for o in targets:
            if self.target_color_attrib in o.data.color_attributes:
                target_color_idx : int = -1
                for i, col in enumerate(o.data.color_attributes):
                    if col.name == self.target_color_attrib:
                        target_color_idx = i
                o.data.color_attributes.render_color_index = target_color_idx

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
OPERATORS : tuple[Operator] = (ABBU_OT_AddColorAttrib,
                               ABBU_OT_DeleteColorAttribs,
                               ABBU_OT_RenameColorAttribs,
                               ABBU_OT_SetActiveColorAttrib,
                               ABBU_OT_SetRenderColorAttrib)
PROPERTIES : tuple[PropertyGroup] = (ABBU_PT_Color_Attrib_Selection,)
