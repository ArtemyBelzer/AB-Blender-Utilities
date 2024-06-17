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
from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import Operator

from .categories import CatNaming, PollType

from ..addon import constants
from ..lib.common import get_child_objects
from ..lib.naming import object_name_custom_expr


class ABBU_OT_AppendBoolOpToBoolObjNames(Operator, CatNaming):
    """Appends the boolean operation to the name of boolean objects.\nSelect one or more objects that contain boolean modifiers"""
    bl_idname = "wm.abbu_append_bool_op_to_bool_obj_names"
    bl_label = "Append Bool Operation To Bool Object Names"
    bl_options = {'REGISTER', 'UNDO'}

    category_poll = PollType.OBJ_MESH_SEL

    prefix_length : IntProperty(
        name = "Prefix Length",
        default = 3
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            for mod in o.modifiers:
                if mod.type == 'BOOLEAN':
                    if mod.object:
                        mod.object.name = mod.operation[:self.prefix_length] + mod.object.name
        
        return {'FINISHED'}

class ABBU_OT_CustomExpressionObjRename(Operator, CatNaming):
    """Renames one or more objects using custom expressions"""
    bl_idname = "wm.abbu_custom_expression_object_rename"
    bl_label = "Custom Expression Object Rename"
    bl_options = {'REGISTER', 'UNDO'}

    category_poll = PollType.OBJ_SEL

    auto_index_on_multiple : BoolProperty(
        name = "Auto index on multiple",
        default = False
    )

    active_object_display : StringProperty(
        name = "Active Object",
        default = ""
    )

    num_splitter : StringProperty(
        name = "Splitter",
        default = ".",
        description = "Splitter that is used for custom expression renaming.\n\
        Ex: \"ObjectName<splitter>01\", \
        \"ObjectName<splitter>02\""
    )

    obj_name : StringProperty(
        name = "New Name",
        default = "",
    )

    padding : IntProperty(
        name = "Zero Padding Count",
        default = 3
    )

    rename_obj_data : BoolProperty(
        name = "Rename object data",
        default = True
    )

    reverse_sort_selected : BoolProperty(
        name = "Reverse sort selected",
        default = False
    )

    sort_selected : BoolProperty(
        name = "Sort selected",
        default = True
    )

    should_split_num : BoolProperty(
        name = "Add splitter before index",
        default = True
    )

    count_index_by_type : BoolProperty(
        name = "Count index by type",
        default = True
    )

    update_multi_user_mesh_data : BoolProperty(
        name = "Update multi-user mesh data names",
        default = False
    )

    def _rename_object(self, o : bpy.types.Object, index : int, num_splitter : str):
        auto_index_str : str = str(index + 1).zfill(self.padding)
        new_name, oidx_found = object_name_custom_expr(o, self.obj_name, str(index + 1))
        o.name = new_name

        # Auto index
        if len(bpy.context.selected_objects) > 1 and self.auto_index_on_multiple and not oidx_found:
            o.name += num_splitter + auto_index_str

        # Object data
        if o.data and self.rename_obj_data:
            if o.data.users > 1 and not self.update_multi_user_mesh_data:
                return
            o.data.name = o.name

    def execute(self, context):
        selected_objects : list[bpy.types.Object] = bpy.context.selected_objects.copy()
        if self.sort_selected:
            selected_objects.sort(key = lambda o : o.name, reverse = self.reverse_sort_selected)

        num_splitter : str = self.num_splitter if self.should_split_num else ""

        if not self.count_index_by_type:
            for i, o in enumerate(selected_objects):
                self._rename_object(o, i, num_splitter)
        else:
            obj_by_type = dict()
            for o in selected_objects:
                if o.type not in obj_by_type:
                    obj_by_type.update({o.type : [o,]})
                else:
                    obj_by_type[o.type].append(o)
            for key, obj_list in obj_by_type.items():
                for i, o in enumerate(obj_list):
                    self._rename_object(o, i, num_splitter)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        
    def draw(self, context):
        active_object : bpy.types.Object = bpy.context.active_object

        layout = self.layout

        layout.prop(self, "obj_name")

        settings_box = layout.box()

        settings_box.prop(self, "count_index_by_type")
        settings_box.prop(self, "auto_index_on_multiple")
        if self.auto_index_on_multiple:
            settings_box.prop(self, "should_split_num")
            if self.should_split_num:
                settings_box.prop(self, "num_splitter")
            settings_box.prop(self, "padding")

        settings_box.prop(self, "rename_obj_data")
        if self.rename_obj_data:
            settings_box.prop(self, "update_multi_user_mesh_data")

        settings_box.prop(self, "sort_selected")
        if self.sort_selected:
            settings_box.prop(self, "reverse_sort_selected")

        box = layout.box()
        object_count : int = len(bpy.context.selected_objects)
        object_suffix : str = "s" if object_count > 1 else ""

        box.label(text = str(object_count) + " object" + object_suffix + " selected.")

        self.active_object_display = active_object.name

        box.label(text = "Active Object: " + active_object.name)
        box.enabled = False

class ABBU_OT_ObjectNamesFromParent(Operator, CatNaming):
    """Renames child objects to match the naming of the parent object"""
    bl_idname = "wm.abbu_object_names_from_parent"
    bl_label = "Object Names From Parent"
    bl_options = {'REGISTER', 'UNDO'}

    category_poll = PollType.OBJ_SEL

    is_recursive : BoolProperty(
        name = "Recursive",
        default = True
    )

    rename_wireframe : BoolProperty(
        name = "Rename wireframe",
        default = True,
    )
    
    rename_mesh_data : BoolProperty(
        name = "Rename Mesh Data",
        default = True,
    )

    bake_suffix_after_idx : BoolProperty(
        name = "Append bake suffix after index",
        description = "Tries to find any bake suffixes in the parent object's name and attempts to append them to the child object after the index",
        default = True,
    )

    number_padding : IntProperty(
        name = "Number Padding",
        default = 3)

    number_splitter : StringProperty(
        name = "Number Splitter",
        default = ".")

    def execute(self, context):        
        for o in bpy.context.selected_objects:
            obj_name_split : list = o.name.split("/")
            obj_name : str = obj_name_split[len(obj_name_split)-1]
            obj_alias : str = ""
            
            if self.bake_suffix_after_idx:
                for alias in constants.bake_suffixes:
                    if alias in obj_name:
                        obj_alias = alias
                        obj_name = obj_name.replace(alias, "")
                        break
            
            children : list[bpy.types.Object] = get_child_objects(o, self.rename_wireframe, self.is_recursive)
            for i, ch_obj in enumerate(children):
                ch_obj.name = obj_name + self.number_splitter + str(i+1).zfill(self.number_padding) + obj_alias
                if ch_obj.data and self.rename_mesh_data:
                    ch_obj.data.name = ch_obj.name

        return {'FINISHED'}

class ABBU_OT_UpdateDataName(Operator, CatNaming):
    """Updates the data name (if present) of one or more selected objects to match the object name"""
    bl_idname = "wm.abbu_update_data_name"
    bl_label = "Update Data Name From Object Name"
    bl_options = {'REGISTER', 'UNDO'}
    
    update_multi_user_data : BoolProperty(
        name = "Update multi-user data names",
        default = False
    )
    
    category_poll = PollType.OBJ_SEL

    def execute(self, context):
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                if o.data.users > 1 and not self.update_multi_user_data:
                    continue
                o.data.name = o.name
                        
        return {'FINISHED'}

OPERATORS : tuple[Operator] = (ABBU_OT_AppendBoolOpToBoolObjNames,
                               ABBU_OT_CustomExpressionObjRename,
                               ABBU_OT_ObjectNamesFromParent,
                               ABBU_OT_UpdateDataName)
