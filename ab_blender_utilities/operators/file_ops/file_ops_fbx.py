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

import mathutils
from ..categories import CatFileFBX
from ...addon import constants, persistent
from ...lib import common, quick_export, fbx_files


def _process_export_object(operator, obj):
    # Selection
    common.deselect_all()
    obj.select_set(True)
                
    bpy.context.view_layer.objects.active = obj
    active_object : bpy.types.Object = obj
    child_objects = common.select_child_objects(operator.export_wire_objects, recursive = operator.recursive_export)
    
    renamed_child_objects : list = []

    for child_object in child_objects:
        if "/" in child_object.name:  # Name is path
            child_object_entry : dict = {}
            child_object_entry["ref"] = child_object
            child_object_entry["old_name"] = child_object.name
            child_object_name_split = child_object.name.split("/")
            child_object.name = child_object_name_split[len(child_object_name_split) - 1]
            renamed_child_objects.append(child_object_entry)

    prefs = persistent.get_preferences()
    if len(prefs.quick_export_name_collection) > 0:
        quick_export.select_objects_from_name_collection(prefs.quick_export_name_collection)

    # Location & rotation
    location : mathutils.Vector = active_object.location.copy()
    rotation : mathutils.Euler = active_object.rotation_euler.copy()
    active_object.location = mathutils.Vector((0.0, 0.0, 0.0))
    active_object.rotation_euler = mathutils.Euler((0.0, 0.0, 0.0))

    # Export name
    export_name : str = active_object.name
    for x in constants.bake_suffixes:
        export_name = export_name.replace(x, "")

    # Remove path from object name
    old_name : str = obj.name
    obj.name = common.get_name_from_path(obj)
                
                
    # FBX export operator
    if persistent.get_preferences().uses_default_export_path:
        quick_export_dir = persistent.get_preferences().default_export_path
    else:
        quick_export_dir = bpy.context.scene[quick_export.export_path_attribute]
    file_path : str = bpy.path.abspath(quick_export_dir)\
    .replace("\\","/")+"/"+export_name+".fbx"
    common.make_directory_from_file_path(file_path)
    fbx_files.export_fbx_file(file_path)
    active_object.location = location
    active_object.rotation_euler = rotation
    # Return old object name
    obj.name = old_name
    
    for child_object in renamed_child_objects:
        child_object["ref"].name = child_object["old_name"]
    
class ABBU_OT_QuickExportFBX(Operator, CatFileFBX):
    """Exports one or more selected objects as FBX files, with an option to include child objects recursively"""
    bl_idname = "export_scene.quick_export_selected_fbx"
    bl_label = "Quick Export As FBX"
    bl_options = {'REGISTER', 'UNDO'}

    restore_selection : BoolProperty(
        name = "Restore Selection",
        description = constants.restore_selection_description,
        default = True
    )

    export_wire_objects : BoolProperty(
        name = "Export Wired",
        description = constants.export_wired_description,
        default = False
    )
    
    recursive_export : BoolProperty(
        name = "Recursive Export",
        default = True)
    
    def execute(self, context):
        if persistent.get_preferences().fbx_exporter_type == 'NATIVE':
            if not quick_export.has_quick_export_path():
                common.warning(self, quick_export.export_path_warning_msg)
                return {'CANCELLED'}

            export_objects : tuple[bpy.types.Object] = bpy.context.selected_objects  # Selected objects

            # Stores the active object in the scene if `restore_selection` is `True`.
            if self.restore_selection:
                active_object_scene : bpy.types.Object = bpy.context.active_object
            
            for o in export_objects:
                _process_export_object(self, o)

            if self.restore_selection:
                common.deselect_all()
                common.select_objects(export_objects)
                bpy.context.view_layer.objects.active = active_object_scene
                    
            return {'FINISHED'}
        else:
            bpy.ops.export_scene.ab_export_custom()
            return {'FINISHED'}
    
OPERATORS : tuple[Operator] = (ABBU_OT_QuickExportFBX,)
