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
from ..lib import ab_common, ab_naming_extra
from ..addon import ab_constants, ab_persistent


class CategoryNaming(ab_common.Category):
    """Operator category class for inheritance"""
    category = "Naming"
    category_arg = ab_common.OperatorCategories.SELECTION
    category_icon = 'GREASEPENCIL'

class OpABObjectNamesFromParent(bpy.types.Operator, CategoryNaming):
    """Renames child objects to match the naming of the parent object"""
    bl_idname = "wm.ab_object_names_from_parent"
    bl_label = "Object names from parent"
    bl_options = {'REGISTER', 'UNDO'}

    recursive : bpy.props.BoolProperty(
        name = "Recursive",
        default = True
    )

    rename_wireframe : bpy.props.BoolProperty(
        name = "Rename wireframe",
        default = True,
    )

    bake_alias_after_idx : bpy.props.BoolProperty(
        name = "Bake alias after index",
        default = True,
    )
    
    def execute(self, context):        
        for obj in bpy.context.selected_objects:
            # Selection
            obj_name_split : list = obj.name.split("/")
            obj_name : str = obj_name_split[len(obj_name_split)-1]
            obj_alias : str = ""
            if self.bake_alias_after_idx:
                for alias in ab_constants.bake_suffixes:
                    if alias in obj_name:
                        obj_alias = alias
                        obj_name = obj_name.replace(alias, "")
                        break
            ab_naming_extra.rename_child_objects(obj, obj_name, obj_alias, self.recursive, self.rename_wireframe)

        return {'FINISHED'}
    
class OpABUpdateMeshData(bpy.types.Operator, CategoryNaming):
    """Update mesh data name"""
    bl_idname = "wm.ab_update_mesh_data"
    bl_label = "Set mesh data name from object name"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if obj.data:
                obj.data.name = obj.name      
                        
        return {'FINISHED'}
    
class OpABFindAndReplaceInName(bpy.types.Operator, CategoryNaming):
    """Finds and replaces a part of a name"""
    bl_idname = "wm.ab_find_and_replace_in_name"
    bl_label = "Find and replace in object name"
    bl_options = {'REGISTER', 'UNDO'}

    obj_find_name : bpy.props.StringProperty(
        name = "Find",
        default = "",
    )

    obj_replace_name : bpy.props.StringProperty(
        name = "Replace",
        default = "",
    )

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj.name = obj.name.replace(self.obj_find_name, self.obj_replace_name)
            if obj.data:
                obj.data.name = obj.name     
                        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class OpABAutoRename(bpy.types.Operator, CategoryNaming):
    """Auto renames objects"""
    bl_idname = "wm.ab_auto_rename"
    bl_label = "Auto/Advanced Rename"
    bl_options = {'REGISTER', 'UNDO'}

    obj_name : bpy.props.StringProperty(
        name = "New Name",
        default = "",
    )

    obj_name_suffix : bpy.props.StringProperty(
        name = "Suffix",
        default = "",
    )

    rename_obj_data : bpy.props.BoolProperty(
        name = "Rename Object Data",
        default = True
    )

    obj_num_splitter : bpy.props.BoolProperty(
        name = "Split index",
        default = True
    )

    active_object_display : bpy.props.StringProperty(
        name = "Active Object",
        default = ""
    )

    padding : bpy.props.IntProperty(
        name = "Zero Padding Count",
        default = 1
    )

    default_loaded : bpy.props.BoolProperty(
        default = False
    )

    def execute(self, context):
        name_splitter = ""
        if self.obj_num_splitter:
            name_splitter = ab_persistent.get_preferences().name_splitter
        
        for i, obj in enumerate(bpy.context.selected_objects):
            index_str : str = ab_common.pad_index(i+1, self.padding)
            object_name : str = ab_naming_extra.object_name_variables(obj, self.obj_name, index_str)
            obj.name = object_name if len(bpy.context.selected_objects) == 1\
                or "$no_index" in self.obj_name\
                or "$index" in self.obj_name\
                else object_name + name_splitter + index_str
            
            if self.obj_name_suffix != "":
               obj.name += ab_naming_extra.object_name_variables(obj, self.obj_name_suffix, index_str)
            
            if obj.data and self.rename_obj_data:
                obj.data.name = obj.name
                        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        if not self.default_loaded:
            self.padding = ab_persistent.get_preferences().name_padding
            self.default_loaded = True
        return context.window_manager.invoke_props_dialog(self)
        
    def draw(self, context):
        selected_objects : list[bpy.types.Object] = bpy.context.selected_objects
        active_object : bpy.types.Object = bpy.context.active_object

        layout = self.layout

        layout.prop(self, "obj_name")
        layout.prop(self, "obj_name_suffix")

        settings_box = layout.box()

        settings_box.prop(self, "rename_obj_data")
        settings_box.prop(self, "obj_num_splitter")
        settings_box.prop(self, "padding")


        box = layout.box()
        object_count : int = len(selected_objects)
        object_suffix : str = "s" if object_count > 1 else ""

        box.label(text = f"{object_count} selected object{object_suffix}")
        # box.label(text = f"Active Object Name")
        self.active_object_display = active_object.name
        # box.prop(self, "active_object_display", emboss = False, text = "Active Object: ")
        box.label(text = f"Active Object: {active_object.name}")
        box.enabled = False

class OpABAppendBooleanOperationToName(bpy.types.Operator, ab_common.Category):
    """Reorders object data alphabetically.\nUseful for the FBX export order"""
    bl_idname = "wm.ab_append_boolean_operation_to_name"
    bl_label = "Append boolean operation to boolean object names"
    bl_options = {'REGISTER', 'UNDO'}

    category = "Naming"
    category_arg = ab_common.OperatorCategories.SELECTION

    prefix_length : bpy.props.IntProperty(
        name = "Prefix Length",
        default = 3
    )

    def execute(self, context):
        for obj in ab_common.get_selected_objects():
            for modifier in obj.modifiers:
                if hasattr(modifier, "object") and hasattr(modifier, "operation"):
                    if modifier.object:
                        modifier.object.name = f"{modifier.operation[:self.prefix_length]}_{modifier.object.name}"
        
        return {'FINISHED'}

OPERATORS : tuple[bpy.types.Operator] = (OpABAutoRename,
                                         OpABFindAndReplaceInName,
                                         OpABObjectNamesFromParent,
                                         OpABUpdateMeshData,
                                         OpABAppendBooleanOperationToName)
