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
from bpy.props import BoolProperty
from bpy.types import Operator

from .categories import CatObjectRot, PollType
from ..lib import common, rot_save


class ABBU_OT_RotPropRestore(Operator, CatObjectRot):
    """Restores the rotation of one or more objects"""
    bl_idname = "object.abbu_rot_prop_restore"
    bl_label = "Restore Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for o in bpy.context.selected_objects:
            rot_save.restore_rotation_in_attribute(o)

        return {'FINISHED'}

class ABBU_OT_RotPropStore(Operator, CatObjectRot):
    """Stores the rotation of one or more objects"""
    bl_idname = "object.abbu_rot_prop_store"
    bl_label = "Store Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    clear_rot : BoolProperty(
        name = "Clear Rotation",
        default = True
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            rot_save.save_rotation_in_attribute(self, o, self.clear_rot)

        return {'FINISHED'}

OPERATORS : tuple[Operator] = (ABBU_OT_RotPropRestore,
                               ABBU_OT_RotPropStore)
