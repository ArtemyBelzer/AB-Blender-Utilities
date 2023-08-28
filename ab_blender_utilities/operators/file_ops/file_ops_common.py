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
import bpy_extras
import mathutils
import types
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ...lib import ab_common, ab_json, ab_quick_export


class CategoryFile(ab_common.Category):
    """Operator category class for inheritance"""
    category = "File"
    category_icon = 'CURRENT_FILE'

class OpABSetUtilityQuickExportPath(bpy.types.Operator, bpy_extras.io_utils.ImportHelper, CategoryFile):
    """Opens a file browser so you can set the export directory"""
    bl_idname = "wm.ab_set_utility_quick_export_path"
    bl_label = "Set quick export path"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True
    
    directory : bpy.props.StringProperty(
        name = "Export Path",
        description = "Quick export directory path",
        subtype='DIR_PATH'
    )

    filter_glob: bpy.props.StringProperty(
        default="",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        bpy.context.scene[ab_quick_export.export_path_attribute] = bpy.path.relpath(self.directory)

        return {'FINISHED'}
    
class OpABExportPointCloudFile(bpy.types.Operator, ExportHelper, CategoryFile):
    """Exports currently selected objects as a point cloud"""
    bl_idname = "export_scene.ab_export_to_point_cloud_file"
    bl_label = "Export Point Cloud"
    bl_options = {'REGISTER'}
    bl_menu_label = "Point Cloud (.json)"

    category_arg = ab_common.OperatorCategories.SELECTION

    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'}, maxlen=255)

    category = "File/Point Cloud"
    
    def execute(self, context):
        data : list = []

        for obj in ab_common.get_selected_objects():
            asset_path = ""
            if "asset_path" in obj:
                asset_path = obj["asset_path"]
            point = ab_json.PointCloudPoint(location = (obj.location.x, obj.location.y, obj.location.y),
                                            rotation = (obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z),
                                            asset_path = asset_path)
            
            data.append(point)
        
        file_handle : types.TextIOWrapper = open(self.filepath, 'w')
        file_handle.write(ab_json.dump_pc_data(data))  # Write JSON string to file
        file_handle.close()

        return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(OpABExportPointCloudFile.bl_idname, text=OpABExportPointCloudFile.bl_menu_label)

class OpABImportPointCloudFile(bpy.types.Operator, ImportHelper, CategoryFile):
    """Imports point cloud and creates instance objects"""
    bl_idname = "import_scene.ab_import_point_cloud_file"
    bl_label = "Import Point Cloud"
    bl_options = {'REGISTER'}
    bl_menu_label = "Point Cloud (.json)"

    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'}, maxlen=255)

    category = "File/Point Cloud"
    
    def execute(self, context):
        with open(self.filepath, 'r') as file_handle:
            data : list | None = ab_json.load_pc_data(file_handle.read())

            if data is None:
                ab_common.error(self, "Invalid point cloud data.")
                return {'CANCELLED'}
            
            active_obj : tuple[bpy.types.Object] = bpy.context.active_object

            if active_obj:
                if active_obj.type == "MESH":
                    for i, data_point in enumerate(data):
                        point_pos = mathutils.Vector(data_point[0])
                        point_rot = mathutils.Vector(data_point[1])
                        new_inst = bpy.data.objects.new("SMI_"+active_obj.name+"_{}".format(ab_common.pad_index(i+1)), 
                                                        active_obj.data)
                        bpy.context.collection.objects.link(new_inst)
                        new_inst.location = point_pos
                        new_inst.rotation_euler = point_rot
                        if data_point[2] != "":
                            new_inst["asset_path"] = data_point[2]
                else:
                    ab_common.warning(self, "You need a \'MESH\' object select to instantiate")
                    return {'CANCELED'}
            else:
                ab_common.warning(self, "No active object selected, unable to instantiate")
                return {'CANCELED'}
        return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(OpABImportPointCloudFile.bl_idname, text=OpABImportPointCloudFile.bl_menu_label)

OPERATORS : tuple[bpy.types.Operator] = (OpABSetUtilityQuickExportPath,
                                         OpABExportPointCloudFile,
                                         OpABImportPointCloudFile)
EXPORTERS : tuple[bpy.types.Operator] = (OpABExportPointCloudFile,)
IMPORTERS : tuple[bpy.types.Operator] = (OpABImportPointCloudFile,)
