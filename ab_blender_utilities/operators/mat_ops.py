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
from bpy.types import Operator
from .categories import (PollType, CatCleanupMat)


class ABBU_OT_RemoveUnusedMaterialSlots(Operator, CatCleanupMat):
    """Removes unused materials from the selected objects"""
    bl_idname = "object.abbu_remove_unused_material_slots"
    bl_label = "Remove Unused Material Slots"
    bl_options = {'REGISTER', 'UNDO'}

    category_poll = PollType.OBJ_SEL
    
    def execute(self, context):
        if bpy.app.version >= (4, 0, 0):
            bpy.ops.object.material_slot_remove_unused()
        else:
            for o in bpy.context.selected_objects:
                if o.type == 'MESH':
                    bpy.ops.object.material_slot_remove_unused({"object": o})

        return {'FINISHED'}

OPERATORS : tuple[Operator] = (ABBU_OT_RemoveUnusedMaterialSlots,)
