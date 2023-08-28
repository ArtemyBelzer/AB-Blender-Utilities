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

def get_linked_cached_objects(obj : bpy.types.Object, *,
                              linked_objects : list[bpy.types.Object] = None)\
                              -> tuple[bpy.types.Object]:
    """Gets all the linked cached objects from the currently selected object.
    Returns a `tuple` of `bpy.types.Object`."""
    if linked_objects == None:
        linked_objects : list[bpy.types.Object] = []
    
    if "ab_cached_object" in obj:
        linked_objects.append(obj["ab_cached_object"])
        get_linked_cached_objects(obj["ab_cached_object"],
                                  linked_objects = linked_objects)

    return tuple(linked_objects)