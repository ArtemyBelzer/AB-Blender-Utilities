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

from mathutils import Vector
from . import common


saved_rot_prop_name = "abbu_saved_rot"

def save_rotation_in_attribute(op : Operator, o : bpy.types.Object, clear_rot : bool) -> None:
    """Stores the rotation inside an attribute of an object and zeroes out the rotation."""
    if not saved_rot_prop_name in o:
        o[saved_rot_prop_name] = o.rotation_euler.copy()
        if clear_rot:
            o.rotation_euler = Vector((0.0, 0.0, 0.0))
    else:
        print(common.warning(op, "save_rotation_in_attribute(" + o.name + ") can not store rotation. Rotation is already stored in this object."))

def restore_rotation_in_attribute(o : bpy.types.Object) -> None:
    """Restores the rotation stored in an attribute."""
    if saved_rot_prop_name in o:
        o.rotation_euler = o[saved_rot_prop_name]
        del o[saved_rot_prop_name]
