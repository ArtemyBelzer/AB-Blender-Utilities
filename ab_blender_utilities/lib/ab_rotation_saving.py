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
import mathutils
from . import ab_common

def store_rotation_in_attribute(op : bpy.types.Operator, obj : bpy.types.Object) -> None:
    """Stores the rotation inside an attribute of an object and zeroes out the rotation."""
    if not "ab_stored_rotation" in obj:
        obj["ab_stored_rotation"] = obj.rotation_euler.copy()
        obj.rotation_euler = mathutils.Vector((0.0, 0.0, 0.0))
    else:
        print(ab_common.warning(op, f"store_rotation_in_attribute({obj.name}) \
                                can not store rotation. Rotation is already stored in this object."))

def restore_rotation_in_attribute(obj : bpy.types.Object) -> None:
    """Restores the rotation stored in an attribute."""
    if "ab_stored_rotation" in obj:
        obj.rotation_euler = obj["ab_stored_rotation"]
        del obj["ab_stored_rotation"]
