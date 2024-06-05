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


def get_col_attrib_count(targets : tuple[bpy.types.Object] |
                         list[bpy.types.Object] = None,
                         unique : bool = True) -> int:
    """Returns the Color Attribute count.
    If `unique` is `True`, then only the attributes with unique names will be counted."""
    color_attrib_count : int = 0
    color_attrib_names_unique : set[str] = set({})

    for o in targets:
        if o.type == 'MESH':
            if o.data.color_attributes:
                if not unique:
                    color_attrib_count += len(o.data.color_attributes)
                else:
                    for col in o.data.color_attributes:
                        color_attrib_names_unique.add(col.name)
    
    if unique:
        color_attrib_count = len(color_attrib_names_unique)

    return color_attrib_count

def get_unique_color_attrib_names_from_selected(targets : tuple[bpy.types.Object] |
                         list[bpy.types.Object] = None) -> tuple[str]:
    """Returns color attribute names from currently selected objects."""
    color_attrib_names_unique : set[str] = set({})
    for o in targets:
        for uv in o.data.color_attributes:
            color_attrib_names_unique.add(uv.name)

    return tuple(color_attrib_names_unique)

def unique_color_attribute_list(self, context) -> list[tuple[str]]:
    color_options : list[tuple[str]]= []
    color_attributes : tuple[str] = get_unique_color_attrib_names_from_selected(targets = bpy.context.selected_objects)
    
    for i, col in enumerate(color_attributes):
        color_options.append((col, col, '', 'GROUP_VCOL', i))
    return sorted(color_options,
                  key = lambda x : x[0],
                  reverse = False)
