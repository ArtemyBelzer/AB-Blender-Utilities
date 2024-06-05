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
from bpy.props import EnumProperty
from bpy.types import Operator

from ..lib import quick_export
from ..addon import keymaps, persistent
from ..addon.constants import e_add_remove


class ABBU_OT_DeleteQuickExportPaths(Operator):
    """Clears any quick export paths from the current Blend file"""
    bl_idname = "wm.abbu_delete_quick_export_paths"
    bl_label = "Delete quick export attributes from scenes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for scene in bpy.data.scenes:
            if quick_export.has_quick_export_path(scene):
                del scene[quick_export.export_path_attribute]
        return {'FINISHED'}
    
class ABBU_OT_RestoreDefaultKeymaps(Operator):
    """Restores the default keymap"""
    bl_idname = "wm.abbu_restore_default_keymaps"
    bl_label = "AB Utilities - Restore Default Keymaps"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        keymaps.restore()
        return {'FINISHED'}
    
class ABBU_OT_AddRemoveQuickExportNames(Operator):
    """Adds or removes quick export names"""
    bl_idname = "object.abbu_add_remove_quick_export_names"
    bl_label = "Add/Remove Quick Export Names"
    bl_description = "Adds or removes a string to a list in the plugin's properties."
    bl_options = {'REGISTER'}

    arg : EnumProperty(
        items = e_add_remove
    )

    def invoke(self, context, event):
        prefs = persistent.get_preferences()
        if self.arg == "ADD":
            name_entry = prefs.quick_export_name_collection.add()
            name_entry.name = "Default"
            name_entry.type = 1
            return {'FINISHED'}
        elif self.arg == "REMOVE":
            entry_idx = prefs.panel_vars_ptr.quick_export_name_selection
            prefs.panel_vars_ptr.quick_export_name_selection -=1
            prefs.quick_export_name_collection.remove(entry_idx)
            return {'FINISHED'}
    
OPERATORS : tuple[Operator] = (ABBU_OT_AddRemoveQuickExportNames,
                               ABBU_OT_DeleteQuickExportPaths,
                               ABBU_OT_RestoreDefaultKeymaps)
