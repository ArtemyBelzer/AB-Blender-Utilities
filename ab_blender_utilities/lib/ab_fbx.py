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
from ..addon import ab_persistent
from typing import Final

exporter_type : Final[tuple[tuple]]= (('NATIVE', "Native FBX", ""),
                                      ('CUSTOM', "Custom", ""))

scale_options : Final[tuple[tuple]]= (('FBX_SCALE_NONE', "None", "FBX_SCALE_NONE"),
                                      ('FBX_SCALE_UNITS', "Units", "FBX_SCALE_UNITS"),
                                      ('FBX_SCALE_CUSTOM', "Custom", "FBX_SCALE_CUSTOM"),
                                      ('FBX_SCALE_ALL', "All", "FBX_SCALE_ALL"))

mesh_smooth_types : Final[tuple[tuple]]= (('OFF', "Off/Vertex", ""),
                                          ('FACE', "Face", ""),
                                          ('EDGE', "Edge", ""))

color_types : Final[tuple[tuple]]= (('NONE', "None", ""),
                                    ('SRGB', "sRGB", ""),
                                    ('LINEAR', "Linear", ""))

def export_fbx_file(file_path : str) -> None:
    """Exports an FBX file based on the current selection."""
    prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()
    object_types : set = set()

    if prefs.fbx_exporter_type == 'NATIVE':

        # Populate object types
        if prefs.native_fbx_ex_export_empty:
            object_types.add('EMPTY')
        if prefs.native_fbx_ex_export_camera:
            object_types.add('CAMERA')
        if prefs.native_fbx_ex_export_light:
            object_types.add('LIGHT')
        if prefs.native_fbx_ex_export_armature:
            object_types.add('ARMATURE')
        if prefs.native_fbx_ex_export_mesh:
            object_types.add('MESH')
        if prefs.native_fbx_ex_export_other:
            object_types.add('OTHER')

        bpy.ops.export_scene.fbx(filepath = file_path,
                                check_existing = prefs.native_fbx_ex_check_existing,
                                use_selection = True,
                                apply_scale_options = prefs.native_fbx_ex_scale_options,
                                object_types = object_types,
                                mesh_smooth_type = prefs.native_fbx_ex_mesh_smooth_type,
                                use_tspace = prefs.native_fbx_ex_use_tspace,
                                use_custom_props = prefs.native_fbx_ex_use_custom_props,
                                add_leaf_bones = False)
        