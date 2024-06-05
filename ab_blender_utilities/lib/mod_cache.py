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

from typing import Final


cached_obj_prop_name : Final[str] = "abbu_cached_object"

def get_linked_cached_objects(o : bpy.types.Object, *,
                              linked_objects : list[bpy.types.Object] = None)\
                              -> tuple[bpy.types.Object]:
    """Gets all the linked cached objects from the currently selected object.
    Returns a `tuple` of `bpy.types.Object`."""
    if linked_objects == None:
        linked_objects : list[bpy.types.Object] = []

    if cached_obj_prop_name in o:
        linked_objects.append(o[cached_obj_prop_name])
        get_linked_cached_objects(o[cached_obj_prop_name],
                                  linked_objects = linked_objects)

    return tuple(linked_objects)

def parent_and_keep_transform(parent : bpy.types.Object, child : bpy.types.Object):
    child_matrix = child.matrix_world.copy()
    child.parent = parent
    child.matrix_world = child_matrix