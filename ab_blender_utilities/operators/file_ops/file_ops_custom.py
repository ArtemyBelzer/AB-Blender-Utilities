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
from ...lib import ab_common, ab_quick_export
from ...addon import ab_persistent

class OpABExportCustom(bpy.types.Operator):
    """Starts a quick export operation"""
    bl_idname = "export_scene.ab_export_custom"
    bl_label = "Custom Export"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Available for custom implementation"""
        if ab_persistent.get_preferences().fbx_exporter_type == 'CUSTOM':
            ab_common.warning(self, "Custom operator not yet implemented.")
            return {'FINISHED'}
        
        return {'CANCELED'}
    
OPERATORS : tuple[bpy.types.Operator] = (OpABExportCustom,)