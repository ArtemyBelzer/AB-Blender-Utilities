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

from .categories import (PollType, CatSel, CatSelSaving)
from ..lib import common


_saved_obj_sel = []

class ABBU_OT_SelectChildObjects(Operator, CatSel):
    """Selects all child objects from the current object selection.\nThis operator can select objects recursively"""
    bl_idname = "object.abbu_select_child_objects"
    bl_label = "Select Child Objects"
    bl_options = {'REGISTER', 'UNDO'}

    recursive : BoolProperty(
        name = "Recursive",
        default = True
    )
    
    select_wireframe : BoolProperty(
        name = "Select wireframe",
        default = True,
    )

    def execute(self, context):
        common.select_child_objects(self.select_wireframe, self.recursive)  
        return {'FINISHED'}

class ABBU_OT_DeleteSavedObjectSelection(Operator, CatSelSaving):
    """Deletes saved object selections created by the \"Save Object Selection\" operator"""
    bl_idname = "wm.abbu_delete_saved_object_selection"
    bl_label = "Delete Saved Selection"
    bl_options = {'REGISTER', 'UNDO'}

    category_poll = PollType.CUSTOM

    @classmethod
    def poll(cl, context):
        return len(_saved_obj_sel) > 0

    def execute(self, context):
        _saved_obj_sel.clear()
        return {'FINISHED'}

class ABBU_OT_RestoreSavedObjectSelection(Operator, CatSelSaving):
    """Restores the saved object selections"""
    bl_idname = "wm.abbu_restore_saved_object_selection"
    bl_label = "Restore Object Selection"
    bl_options = {'REGISTER', 'UNDO'}

    category_poll = PollType.CUSTOM

    @classmethod
    def poll(cl, context):
        return len(_saved_obj_sel) > 0

    def execute(self, context):
        for o in _saved_obj_sel:
            if o.name in bpy.data.objects:
                o.select_set(True)
        return {'FINISHED'}

class ABBU_OT_SaveObjectSelection(Operator, CatSelSaving):
    """Saves the currently selected objects. These selections can be restored using the \"Restore Object Selection\" operator"""
    bl_idname = "wm.abbu_save_object_selection"
    bl_label = "Save Object Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global _saved_obj_sel
        _saved_obj_sel = bpy.context.selected_objects
        return {'FINISHED'}

OPERATORS : tuple[Operator] = (ABBU_OT_SelectChildObjects,
                               ABBU_OT_DeleteSavedObjectSelection,
                               ABBU_OT_SaveObjectSelection,
                               ABBU_OT_RestoreSavedObjectSelection)
