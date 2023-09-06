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
from ..addon import ab_constants


class CategoryCleanup(ab_common.Category):
    """Operator category class for inheritance"""
    category = "Cleanup"
    category_icon = 'BRUSH_DATA'

class OpABRemoveUnusedMaterialsOnSelected(bpy.types.Operator, CategoryCleanup):
    """Remove unused materials on selected"""
    bl_idname = "object.ab_remove_unused_materials_on_selected"
    bl_label = "Remove unused materials"
    bl_options = {'REGISTER', 'UNDO'}

    category_arg = ab_common.OperatorCategories.SELECTION
    
    def execute(self, context):        
        for obj in bpy.context.selected_objects:
            if obj.data:
                if hasattr(obj.data, "materials"):
                    bpy.ops.object.material_slot_remove_unused({"object": obj})

        return {'FINISHED'}
    
class OpABGlobalCleanup(bpy.types.Operator, CategoryCleanup):
    """Cleanup unused data blocks"""
    bl_idname = "wm.ab_global_cleanup"
    bl_label = "Global cleanup"
    bl_options = {'REGISTER', 'UNDO'}

    category_arg = ab_common.OperatorCategories.CUSTOM

    @classmethod
    def poll(cls, context):
        for block_type in ab_constants.block_types:
            for block in getattr(bpy.data, block_type):
                if block.users == 0:
                    return True
        return False
    
    def execute(self, context):
        stats : dict = {}
        for block_type in ab_constants.block_types:
            stats[block_type] = 0
            for block in getattr(bpy.data, block_type):
                if block.users == 0:
                    stats[block_type] += 1
                    getattr(bpy.data, block_type).remove(block)
            if stats[block_type] > 0:
                suffix : str = "s" if stats[block_type] > 1 else ""
                info_msg : str = f"Removed {stats[block_type]} block{suffix} of \"{block_type}\" type."
                print(ab_common.info(self, info_msg))
                
        return {'FINISHED'}
    
OPERATORS : tuple[bpy.types.Operator] = (OpABRemoveUnusedMaterialsOnSelected,
                                         OpABGlobalCleanup)
