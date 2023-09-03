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

"""
Common functions shared between different operators
"""
import bpy
import subprocess
import os
from enum import Enum
from ..addon import ab_constants


class OperatorCategories(Enum):
    """Operator categories for the Category class in the `ab_common` module."""
    NONE = 0  # No check if performed with this category.
    SELECTION = 1  # If the current selection is < 1, the operator is disabled.
    CUSTOM = 2

class Category():
    """Category class for operators"""
    category : str = ""
    category_arg : OperatorCategories = OperatorCategories.NONE
    category_icon : str = None

    @classmethod
    def poll(cls, context):
        if cls.category_arg == OperatorCategories.SELECTION:
            return len(context.selected_objects) > 0
        return True
    
class PropertiesDialog():
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

# Operator reports

def info(operator : bpy.types.Operator, msg : str) -> str:
    """Reports Blender info from the operator.\n
    Returns a string with the message for printing."""
    msg : str = f"{ab_constants.info}{msg}"
    if operator is not None:
        operator.report({'INFO'}, msg)
    return msg

def warning(operator : bpy.types.Operator, msg : str) -> str:
    """Reports a Blender warning from the operator.\n
    Returns a string with the message for printing."""
    msg : str = f"{ab_constants.warning}{msg}"
    if operator is not None:
        operator.report({'WARNING'}, msg)
    return msg

def error(operator : bpy.types.Operator, msg : str) -> str:
    """Reports a Blender error from the operator.\n
    Returns a string with the message for printing."""
    msg : str = f"{ab_constants.error}{msg}"
    if operator is not None:
        operator.report({'ERROR'}, msg)
    return msg

# Common functions

def get_name_from_path(target : str) -> str:
    """Returns the name of the object.\n
    This is used with objects that have a path part of their name."""
    return target.name.split("/")[-1:][0]

def copy_string_to_clipboard(value: str) -> int:
    """Copies a string to clipboard."""
    cmd : str = f"echo {value.strip()}|clip"
    return subprocess.check_call(cmd, shell=True)

def get_selected_objects() -> tuple[bpy.types.Object]:
    """Returns an immutable list of selected objects."""
    return tuple(bpy.context.selected_objects)

def select_child_objects(select_wire : bool = False) -> None:
    """Selects all child objects in selected objects.\n
    The `select_wire` argument bypasses the `display_type` check."""
    for obj in bpy.context.selected_objects:
        for ch_obj in obj.children:
            if ch_obj.display_type == 'TEXTURED'\
            or ch_obj.display_type == 'SOLID'\
            or select_wire:
                ch_obj.select_set(True)

def deselect_all() -> None:
    """Deselects all objects."""
    for obj in bpy.context.selected_objects:
        obj.select_set(False)

def get_modifier_objects(obj : bpy.types.Object,
                         select : bool = False) -> tuple[bpy.types.Object]:
    """Get objects referenced in modifiers of an object.\n
    Optionally, the `select` argument allows the selections of objects
    referenced by modifiers."""
    targets : list[bpy.types.Object] = []
    for modifier in obj.modifiers:
        if hasattr(modifier, "object"):
            if modifier.object:
                targets.append(modifier.object)
                if select:
                    modifier.object.select_set(True)
    
    return tuple(targets)

def does_object_exist(obj : bpy.types.Object) -> bool:
    """Returns `True` if the object exists in the scene."""
    if obj:
        try:
            if obj.name in bpy.data.objects:
                return True
        except Exception as e:
            print("Warning: {} does not exist in bpy.data.objects.\n".format(obj, str(e)))
    return False

def pad_index(value : int, padding : int = 1) -> str:
    """Pads an index with extra \'0s\'."""
    return f"{value:0{padding+1}d}"

def make_directory_from_file_path(value : str) -> None:
    """Helper function that creates a directory if the file path contains a folder which does not exist."""
    file_directory : tuple[str, any]= os.path.split(value)
    if not os.path.exists(file_directory[0]):
        os.makedirs(file_directory[0])
