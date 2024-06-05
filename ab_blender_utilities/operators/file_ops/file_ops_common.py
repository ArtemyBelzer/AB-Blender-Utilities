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
import bpy_extras
from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.props import IntProperty, StringProperty
from bpy.types import Operator

import mathutils
from ..categories import CatFile, CatFilePointCloud, PollType
from ...lib import common, point_cloud, quick_export


class ABBU_OT_SetQuickExportDir(Operator, bpy_extras.io_utils.ImportHelper, CatFile):
    """Opens a file browser to set the quick export directory"""
    bl_idname = "wm.abbu_set_quick_export_dir"
    bl_label = "Set Quick Export Directory"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cl, context):
        return True

    directory : StringProperty(
        name = "Export Path",
        description = "Quick export directory path",
        subtype='DIR_PATH'
    )

    filter_glob: StringProperty(
        default="",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        bpy.context.scene[quick_export.export_path_attribute] = bpy.path.relpath(self.directory)

        return {'FINISHED'}

class ABBU_OT_ExportPC(Operator, ExportHelper, CatFilePointCloud):
    """Exports the currently selected objects as a JSON file representing a point cloud"""
    bl_idname = "export_scene.abbu_export_pc"
    bl_label = "Export Point Cloud"
    bl_options = {'REGISTER'}
    bl_menu_label = "Point Cloud (.json)"

    category_poll = PollType.OBJ_SEL

    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={'HIDDEN'}, maxlen=255)
    
    def execute(self, context):
        data : list = []

        for o in bpy.context.selected_objects:
            asset_path = ""
            if "asset_path" in o:
                asset_path = o["asset_path"]
            point = point_cloud.PointCloudPoint(location = (o.location.x, o.location.y, o.location.z),
                                            rotation = (o.rotation_euler.x, o.rotation_euler.y, o.rotation_euler.z),
                                            scale = (o.scale.x, o.scale.y, o.scale.z),
                                            asset_path = asset_path)

            data.append(point)

        with open(self.filepath, 'w', encoding = 'utf8') as file_handle:
            file_handle.write(point_cloud.dump_pc_data(data))  # Write JSON string to file

        return {'FINISHED'}

    def menu_func(self, context):
        self.layout.operator(ABBU_OT_ExportPC.bl_idname, text=ABBU_OT_ExportPC.bl_menu_label)

class ABBU_OT_ImportPC(Operator, ImportHelper, CatFilePointCloud):
    """Imports a JSON file containing a point cloud and creates instanced objects.\nAn object must be selected before importing to instantiate from"""
    bl_idname = "import_scene.abbu_import_pc"
    bl_label = "Import Point Cloud"
    bl_options = {'REGISTER'}
    bl_menu_label = "Point Cloud (.json)"

    category_poll = PollType.OBJ_SEL

    number_padding : IntProperty(
        name = "Number Padding",
        default = 3
    )

    number_splitter : StringProperty(
        name = "Name Splitter",
        default = ".")

    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={'HIDDEN'}, maxlen=255)

    def execute(self, context):
        active_obj : tuple[bpy.types.Object] = bpy.context.active_object
        if active_obj == None:
            return {'CANCELED'}

        with open(self.filepath, 'r', encoding = 'utf8') as file_handle:
            data : list | None = point_cloud.load_pc_data(file_handle.read())

            if data is None:
                common.error(self, "Invalid point cloud data.")
                return {'CANCELLED'}
            

            if active_obj:
                if active_obj.type == "MESH":
                    for i, data_point in enumerate(data):
                        point_pos = mathutils.Vector(data_point[0])
                        point_rot = mathutils.Vector(data_point[1])
                        point_scale = mathutils.Vector(data_point[2])
                        new_inst = bpy.data.objects.new(active_obj.name + "_Instance" + self.number_splitter + str(i+1).zfill(self.number_padding), 
                                                        active_obj.data)
                        bpy.context.collection.objects.link(new_inst)
                        new_inst.location = point_pos
                        new_inst.rotation_euler = point_rot
                        new_inst.scale = point_scale
                        if data_point[3] != "":
                            new_inst["asset_path"] = data_point[3]
                else:
                    common.warning(self, "You need a \'MESH\' object select to instantiate")
                    return {'CANCELED'}
            else:
                common.warning(self, "No active object selected, unable to instantiate")
                return {'CANCELED'}
        return {'FINISHED'}

    def menu_func(self, context):
        self.layout.operator(ABBU_OT_ImportPC.bl_idname, text=ABBU_OT_ImportPC.bl_menu_label)

OPERATORS : tuple[Operator] = (ABBU_OT_SetQuickExportDir,
                               ABBU_OT_ExportPC,
                               ABBU_OT_ImportPC)
EXPORTERS : tuple[Operator] = (ABBU_OT_ExportPC,)
IMPORTERS : tuple[Operator] = (ABBU_OT_ImportPC,)
