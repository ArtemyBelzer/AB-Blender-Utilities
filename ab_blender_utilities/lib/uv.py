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


def get_uv_list_from_selected(self, context) -> list[tuple[str]]:
    uv_options : list[tuple[str]]= []
    objs : tuple[bpy.types.Object] = bpy.context.selected_objects
    uvs : tuple[str] = get_uv_names_from_objects(objs)
    
    for i, uv in enumerate(uvs):
        uv_options.append((uv, uv, '', 'GROUP_UVS', i))
    
    return sorted(uv_options,
                  key = lambda x : x[0],
                  reverse = False)

def get_uv_names_from_objects(objs) -> tuple[str]:
    """Returns UV channels from currently selected objects."""
    uvs = []
    for o in objs:
        if o.type == 'MESH':
            for uv in o.data.uv_layers:
                if uv.name not in uvs:
                    uvs.append(uv.name)
    
    return tuple(uvs)
