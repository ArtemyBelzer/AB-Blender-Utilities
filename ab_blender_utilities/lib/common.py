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

"""
Common functions shared between different operators
"""
import bpy
from bpy.types import Operator

import os
from ..addon import constants


class PropertiesDialog():
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

# Operator reports

def info(operator : Operator, msg : str) -> str:
    """Reports Blender info from the operator.\n
    Returns a string with the message for printing."""
    msg : str = constants.info + msg
    if operator is not None:
        operator.report({'INFO'}, msg)
    return msg

def warning(operator : Operator, msg : str) -> str:
    """Reports a Blender warning from the operator.\n
    Returns a string with the message for printing."""
    msg : str = constants.info + msg
    if operator is not None:
        operator.report({'WARNING'}, msg)
    return msg

def error(operator : Operator, msg : str) -> str:
    """Reports a Blender error from the operator.\n
    Returns a string with the message for printing."""
    msg : str = constants.info + msg
    if operator is not None:
        operator.report({'ERROR'}, msg)
    return msg

# Common functions

def get_name_from_path(target : str) -> str:
    """Returns the name of the object.\n
    This is used with objects that have a path part of their name."""
    return target.name.split("/")[-1:][0]

def __select_child_objects(o : bpy.types.Object,
                           select_wire : bool = False,
                           recursive : bool = False) -> None:
    """Selects all child objects in the `obj` argument.\n
    The `select_wire` argument bypasses the `display_type` check."""
    child_objects : list = []
    for ch_obj in o.children:
        if ch_obj.display_type == 'TEXTURED'\
            or ch_obj.display_type == 'SOLID'\
            or select_wire:
                child_objects.append(ch_obj)
                ch_obj.select_set(True)
                if len(ch_obj.children) > 0 and recursive:
                    child_objects += __select_child_objects(ch_obj, select_wire, recursive)
    return child_objects

def select_child_objects(select_wire : bool = False,
                         recursive : bool = False,
                         *,
                         objects : bpy.types.Object = None) -> tuple:
    """Selects all child objects in selected objects.\n
    The `select_wire` argument bypasses the `display_type` check."""
    if objects == None:
        objects = bpy.context.selected_objects
    
    child_objects : list = []
    for o in objects:
        child_objects += __select_child_objects(o, select_wire, recursive)
    return tuple(child_objects)

def get_child_objects(o : bpy.types.Object,
                      select_wire : bool = False,
                      recursive : bool = False) -> list[bpy.types.Object]:
    """Gets all child objects in the `obj` argument.\n
    The `select_wire` argument bypasses the `display_type` check."""
    children : list[bpy.types.Object] = []
    for ch_obj in o.children:
            if ch_obj.display_type == 'TEXTURED'\
            or ch_obj.display_type == 'SOLID'\
            or select_wire:
                children.append(ch_obj)
                if len(ch_obj.children) > 0 and recursive:
                    children += get_child_objects(ch_obj, select_wire, recursive)
    return children

def select_objects(targets : list[bpy.types.Object] | tuple[bpy.types.Object]) -> None:
    """Selects target objects."""
    for o in targets:
        # Selection
        if o:
            o.select_set(True)

def deselect_all() -> None:
    """Deselects all objects."""
    for o in bpy.context.selected_objects:
        o.select_set(False)

def get_modifier_objects(o : bpy.types.Object,
                         select : bool = False) -> tuple[bpy.types.Object]:
    """Get objects referenced in modifiers of an object.\n
    Optionally, the `select` argument allows the selections of objects
    referenced by modifiers."""
    targets : list[bpy.types.Object] = []
    for modifier in o.modifiers:
        if hasattr(modifier, "object"):
            if modifier.object:
                targets.append(modifier.object)
                if select:
                    modifier.object.select_set(True)
    
    return tuple(targets)

def make_directory_from_file_path(value : str) -> None:
    """Helper function that creates a directory if the file path contains a folder which does not exist."""
    file_directory : tuple[str, any]= os.path.split(value)
    if not os.path.exists(file_directory[0]):
        os.makedirs(file_directory[0])
