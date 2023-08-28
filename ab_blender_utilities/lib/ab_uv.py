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
from . import ab_common

def get_uv_channel_count(targets : tuple[bpy.types.Object] |
                         list[bpy.types.Object] = None,
                         unique : bool = True) -> int:
    """Returns the amount of UV channels.
    If `unique` is set to `True` then only the channels with unique names will be counted."""
    uv_channel_count : int = 0
    uv_channel_names_unique : set[str] = set({})
    for obj in targets:
        if obj.data:
            if obj.data.uv_layers:
                if not unique:
                    uv_channel_count += len(obj.data.uv_layers)
                else:
                    for uv in obj.data.uv_layers:
                        uv_channel_names_unique.add(uv.name)
    
    if unique:
        uv_channel_count = len(uv_channel_names_unique)

    return uv_channel_count

def get_unique_uv_channel_names_from_selected(targets : tuple[bpy.types.Object] |
                         list[bpy.types.Object] = None) -> tuple[str]:
    """Returns UV channels from currently selected objects."""
    uv_channel_names_unique : set[str] = set({})
    for obj in targets:
        for uv in obj.data.uv_layers:
                uv_channel_names_unique.add(uv.name)
    
    return tuple(uv_channel_names_unique)

def unique_uv_channel_list(self, context) -> list[tuple[str]]:
    uv_options : list[tuple[str]]= []
    targets : tuple[bpy.types.Object] = ab_common.get_selected_objects()
    uvs : tuple[str] = get_unique_uv_channel_names_from_selected(targets = targets)
    
    for i, uv in enumerate(uvs):
        uv_options.append((uv, uv, '', 'GROUP_UVS', i))
    
    return sorted(uv_options,
                  key = lambda x : x[0],
                  reverse = False)