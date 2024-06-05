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
from bpy.props import CollectionProperty
from bpy.types import Scene

from typing import Final


export_path_attribute : Final[str] = "abbu_quick_export_path"
export_path_warning_msg : Final[str] = "No quick export path was set in the current scene."

def has_quick_export_path(scene : Scene = None) -> bool:
    """Checks if the current scene has a quick export path set.\n
    Returns `True` if the quick export attribute is found"""
    return True if export_path_attribute in bpy.context.scene else False
    
def __select_by_name_collection(o : bpy.types.Object, name_collection):
    for name_item in name_collection:
        if name_item.arg_type == 'CONTAINS':
            if name_item.name in o.name:
                o.select_set(True)
        elif name_item.arg_type == 'BEGINS_WITH':
            if o.name.startswith(name_item.name):
                o.select_set(True)
        elif name_item.arg_type == 'ENDS_WITH':
            if o.name.endswith(name_item.name):
                o.select_set(True)

def select_objects_from_name_collection(name_collection : CollectionProperty, target_object = None) -> None:
    if target_object == None:
        for o in bpy.context.selected_objects:
            for ch_obj in o.children:
                if ch_obj.type == 'MESH':
                    __select_by_name_collection(ch_obj, name_collection)
                if ch_obj.type == 'EMPTY':
                    select_objects_from_name_collection(name_collection, ch_obj)
    else:
        for ch_obj in target_object.children:
            if ch_obj.type == 'MESH':
                __select_by_name_collection(ch_obj, name_collection)
            if ch_obj.type == 'EMPTY':
                select_objects_from_name_collection(name_collection, ch_obj)
