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
from ...addon import ab_constants, ab_persistent
from ...lib import ab_common, ab_quick_export, ab_fbx


class CategoryFileFBX(ab_common.Category):
    """Operator category class for inheritance"""
    category = "File/FBX Quick Export"
    category_arg = ab_common.OperatorCategories.SELECTION

class OpABQuickExportFBX(bpy.types.Operator, CategoryFileFBX):
    """Starts a quick export operation"""
    bl_idname = "export_scene.ab_quick_export_fbx"
    bl_label = "Quick export active as FBX"
    bl_options = {'REGISTER', 'UNDO'}

    restore_selection : bpy.props.BoolProperty(
        name = "Restore Selection",
        description = ab_constants.restore_selection_description,
        default = True
    )

    export_wire_objects : bpy.props.BoolProperty(
        name = "Export Wired",
        description = ab_constants.export_wired_description,
        default = False
    )
    
    def execute(self, context):
        if ab_persistent.get_preferences().fbx_exporter_type == 'NATIVE':
            if not ab_quick_export.has_quick_export_path():
                ab_common.warning(self, ab_quick_export.export_path_warning_msg)
                return {'CANCELLED'}
            
            # Selection
            active_object : bpy.types.Object = bpy.context.active_object
            ab_common.select_child_objects(self.export_wire_objects)

            prefs = ab_persistent.get_preferences()
            if prefs.quick_export_name_collection > 0:
                ab_quick_export.select_objects_from_name_collection()

            # Location & rotation
            location : mathutils.Vector = active_object.location.copy()
            rotation : mathutils.Euler = active_object.rotation_euler.copy()
            active_object.location = mathutils.Vector((0.0, 0.0, 0.0))
            active_object.rotation_euler = mathutils.Euler((0.0, 0.0, 0.0))

            # Export name
            export_name : str = active_object.name

            # Remove path from object name
            old_name : str= active_object.name
            active_object.name : str= ab_common.get_name_from_path(active_object)

            additional_export_directory : str = ""
            if "_BO" in export_name:
                additional_export_directory = "Blockout/"
                export_name = export_name.replace("_BO", "")
                if bpy.context.scene["directory_exclusion"]:
                    export_name = export_name.replace(bpy.context.scene["directory_exclusion"], "")

            # FBX export operator
            if ab_persistent.get_preferences().uses_default_export_path:
                quick_export_dir = ab_persistent.get_preferences().default_export_path
            else:
                quick_export_dir = bpy.context.scene[ab_quick_export.export_path_attribute]
            file_path : str = bpy.path.abspath(quick_export_dir)\
            .replace("\\","/")+"/"+additional_export_directory+export_name+".fbx"
            ab_common.make_directory_from_file_path(file_path)
            ab_fbx.export_fbx_file(file_path)
            active_object.location = location
            active_object.rotation_euler = rotation
            active_object.name = old_name

            if self.restore_selection:
                ab_common.deselect_all()
                active_object.select_set(True)
                bpy.context.view_layer.objects.active = active_object

            return {'FINISHED'}
        else:
            bpy.ops.export_scene.ab_export_custom()
            return {'FINISHED'}
    
class OpABQuickExportSelectedFBX(bpy.types.Operator, CategoryFileFBX):
    """Starts a quick export operation for currently selected objects"""
    bl_idname = "export_scene.ab_quick_export_selected_fbx"
    bl_label = "Quick export selected as FBX"
    bl_options = {'REGISTER', 'UNDO'}

    restore_selection : bpy.props.BoolProperty(
        name = "Restore Selection",
        description = ab_constants.restore_selection_description,
        default = True
    )

    export_wire_objects : bpy.props.BoolProperty(
        name = "Export Wired",
        description = ab_constants.export_wired_description,
        default = False
    )
    
    def execute(self, context):
        if ab_persistent.get_preferences().fbx_exporter_type == 'NATIVE':
            if not ab_quick_export.has_quick_export_path():
                ab_common.warning(self, ab_quick_export.export_path_warning_msg)
                return {'CANCELLED'}

            export_objects : tuple[bpy.types.Object] = ab_common.get_selected_objects()

            # Stores the active object in the scene if `restore_selection` is `True`.
            if self.restore_selection:
                active_object_scene : bpy.types.Object = bpy.context.active_object
            
            for obj in export_objects:
                # Selection
                ab_common.deselect_all()
                obj.select_set(True)
                
                bpy.context.view_layer.objects.active = obj
                active_object : bpy.types.Object = obj
                ab_common.select_child_objects(self.export_wire_objects)

                prefs = ab_persistent.get_preferences()
                if len(prefs.quick_export_name_collection) > 0:
                    ab_quick_export.select_objects_from_name_collection(prefs.quick_export_name_collection)

                # Location & rotation
                location : mathutils.Vector = active_object.location.copy()
                rotation : mathutils.Euler = active_object.rotation_euler.copy()
                active_object.location = mathutils.Vector((0.0, 0.0, 0.0))
                active_object.rotation_euler = mathutils.Euler((0.0, 0.0, 0.0))

                # Export name
                export_name : str = active_object.name
                for x in ab_constants.bake_suffixes:
                    export_name = export_name.replace(x, "")

                # Remove path from object name
                old_name : str = obj.name
                obj.name = ab_common.get_name_from_path(obj)
                
                
                # FBX export operator
                if ab_persistent.get_preferences().uses_default_export_path:
                    quick_export_dir = ab_persistent.get_preferences().default_export_path
                else:
                    quick_export_dir = bpy.context.scene[ab_quick_export.export_path_attribute]
                file_path : str = bpy.path.abspath(quick_export_dir)\
                .replace("\\","/")+"/"+export_name+".fbx"
                ab_common.make_directory_from_file_path(file_path)
                ab_fbx.export_fbx_file(file_path)
                active_object.location = location
                active_object.rotation_euler = rotation
                # Return old object name
                obj.name = old_name

            if self.restore_selection:
                ab_common.deselect_all()
                ab_common.select_objects(export_objects)
                bpy.context.view_layer.objects.active = active_object_scene
                    
            return {'FINISHED'}
        else:
            bpy.ops.export_scene.ab_export_custom()
            return {'FINISHED'}
    
OPERATORS : tuple[bpy.types.Operator] = (OpABQuickExportFBX,
                                         OpABQuickExportSelectedFBX)
