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

def get_color_attribute_channel_count(targets : tuple[bpy.types.Object] |
                                      list[bpy.types.Object] = None,
                                      unique : bool = True) -> int:
    """Returns the amount of Color Attributes.
    If `unique` is set to `True` then only the attributes with unique names will be counted."""
    color_attrib_count : int = 0
    color_attrib_names_unique : set[str] = set({})
    for obj in targets:
        if obj.data:
            if obj.data.color_attributes:
                if not unique:
                    color_attrib_count += len(obj.data.color_attributes)
                else:
                    for col in obj.data.color_attributes:
                        color_attrib_names_unique.add(col.name)
    
    if unique:
        color_attrib_count = len(color_attrib_names_unique)

    return color_attrib_count

def get_unique_color_attrib_names_from_selected(targets : tuple[bpy.types.Object] |
                         list[bpy.types.Object] = None) -> tuple[str]:
    """Returns color attribute names from currently selected objects."""
    color_attrib_names_unique : set[str] = set({})
    for obj in targets:
        for uv in obj.data.color_attributes:
                color_attrib_names_unique.add(uv.name)
    
    return tuple(color_attrib_names_unique)

def unique_color_attribute_list(self, context) -> list[tuple[str]]:
    color_options : list[tuple[str]]= []
    targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
    color_attributes : tuple[str] = get_unique_color_attrib_names_from_selected(targets = targets)
    
    for i, col in enumerate(color_attributes):
        color_options.append((col, col, '', 'GROUP_VCOL', i))
    
    return sorted(color_options,
                  key = lambda x : x[0],
                  reverse = False)

def remove_vertex_colors_from_object(obj : bpy.types.Object) -> None:
    """Removes vertex colors from a referenced object."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.geometry.color_attribute_remove()
    except Exception as e:
        print(f"{ab_constants.error}{e}")
        