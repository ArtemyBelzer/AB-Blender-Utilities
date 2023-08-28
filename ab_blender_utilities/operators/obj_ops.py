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
from ..lib import ab_common

class CategoryBaseObjects(ab_common.Category):
    """Selection base class"""
    category = "Objects"
    category_arg = ab_common.OperatorCategories.SELECTION
    category_icon = 'MESH_CUBE'

class OpABReorderObjectDataAlphabetically(bpy.types.Operator, CategoryBaseObjects):
    """Reorders object data alphabetically.\nUseful for the FBX export order"""
    bl_idname = "wm.ab_reorder_object_data_alphabetically"
    bl_label = "Reorder Object Data Blocks Alphabetically"
    bl_options = {'REGISTER', 'UNDO'}

    reverse : bpy.props.BoolProperty(
        name = "Reverse",
        default = False
    )

    def execute(self, context):
        selected_objects : list[bpy.types.Object] = bpy.context.selected_objects
        selected_objects_ordered : list[bpy.types.Object]= sorted(selected_objects.copy(),
                                                                  key = lambda x: x.name,
                                                                  reverse=self.reverse)

        for ordered_obj_src in selected_objects_ordered:
            copied_obj : bpy.types.Object = ordered_obj_src.copy()
            copied_obj.name : str = ordered_obj_src.name
            copied_obj.data : bpy.types.Mesh = ordered_obj_src.data.copy()
            copied_obj.data.name : str = ordered_obj_src.data.name
            if ordered_obj_src.children:
                for child in ordered_obj_src.children:
                    child.parent = copied_obj
            bpy.context.collection.objects.link(copied_obj)
        
        bpy.ops.object.delete({"selected_objects": selected_objects})
        
        return {'FINISHED'}
    
class OpABReorderModifierObjectDataToModifierOrder(bpy.types.Operator, CategoryBaseObjects):
    """Reorders object data alphabetically.\nUseful for the FBX export order"""
    bl_idname = "wm.ab_reorder_modifier_object_data_to_modifier_order"
    bl_label = "Reorder Modifier Object Data Blocks to Modifier Order"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects_to_delete : list[bpy.types.Object] = []
        for obj in ab_common.get_selected_objects():
            for modifier in obj.modifiers:
                if hasattr(modifier, "object"):
                    if modifier.object:
                        copied_obj : bpy.types.Object = modifier.object.copy()
                        copied_obj.name : str = modifier.object.name
                        copied_obj.data : bpy.types.Mesh = modifier.object.data.copy()
                        copied_obj.data.name : str = modifier.object.data.name
                        if modifier.object.children:
                            for child in modifier.object.children:
                                child.parent = copied_obj
                        if modifier.object.parent:
                            copied_obj.parent = modifier.object.parent
                        bpy.context.collection.objects.link(copied_obj)
                        objects_to_delete.append(modifier.object)
                        modifier.object = copied_obj
        
        bpy.ops.object.delete({"selected_objects": objects_to_delete})
        
        return {'FINISHED'}
    
OPERATORS : tuple[bpy.types.Operator] = (OpABReorderObjectDataAlphabetically,
                                         OpABReorderModifierObjectDataToModifierOrder)
