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
from ..lib import ab_common, ab_selection_saving


class CategorySelection(ab_common.Category):
    """Operator category class for inheritance"""
    category = "Selection"
    category_icon = 'RESTRICT_SELECT_OFF'

class OpABSelectChildObjects(bpy.types.Operator, CategorySelection):
    """Selects all child objects.\nThis operator can select objects recursively"""
    bl_idname = "object.ab_select_all_child_objects"
    bl_label = "Select child objects"
    bl_options = {'REGISTER', 'UNDO'}

    category_arg = ab_common.OperatorCategories.SELECTION

    recursive : bpy.props.BoolProperty(
        name = "Recursive",
        default = True
    )
    
    select_wireframe : bpy.props.BoolProperty(
        name = "Select wireframe",
        default = True,
    )

    def execute(self, context):
        ab_common.select_child_objects(self.select_wireframe, self.recursive)  
        return {'FINISHED'}
    
class OpABSaveSelection(bpy.types.Operator, CategorySelection):
    """Saves the current selection, can be restorted using the \"Restore Selection\" operator"""
    bl_idname = "object.ab_save_selection"
    bl_label = "Save Selection"
    bl_options = {'REGISTER', 'UNDO'}

    category_arg = ab_common.OperatorCategories.SELECTION

    def execute(self, context):
        ab_selection_saving.save_selection()
        return {'FINISHED'}
    
class OpABRestoreSelection(bpy.types.Operator, CategorySelection):
    """Restores a selection saved using the \"Save Selection\" operator"""
    bl_idname = "object.ab_restore_selection"
    bl_label = "Restore Selection"
    bl_options = {'REGISTER', 'UNDO'}

    category_arg = ab_common.OperatorCategories.CUSTOM

    @classmethod
    def poll(cls, context):
        return ab_selection_saving.does_stored_selection_exist()

    def execute(self, context):
        ab_selection_saving.restore_selection()
        return {'FINISHED'}
    
class OpABDeleteSavedSelection(bpy.types.Operator, CategorySelection):
    """Restores a selection saved using the \"Save Selection\" operator"""
    bl_idname = "object.ab_delete_saved_selection"
    bl_label = "Delete Saved Selection"
    bl_options = {'REGISTER', 'UNDO'}

    category_arg = ab_common.OperatorCategories.CUSTOM

    @classmethod
    def poll(cls, context):
        return ab_selection_saving.does_stored_selection_exist()

    def execute(self, context):
        ab_selection_saving.delete_saved_selection()
        return {'FINISHED'}
    
OPERATORS : tuple[bpy.types.Operator] = (OpABSelectChildObjects,
                                         OpABSaveSelection,
                                         OpABRestoreSelection,
                                         OpABDeleteSavedSelection)
