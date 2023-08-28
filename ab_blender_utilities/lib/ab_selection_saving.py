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
from . import ab_common
from ..data import ab_data


def save_selection() -> None:
    """Saves the current selection to the data store"""
    ab_data.saved_selection = bpy.context.selected_objects

def delete_saved_selection() -> bool:
    """Deletes the saved selection.\nReturns `False` if the saved selection does not exist"""
    if ab_data.saved_selection:
        ab_data.saved_selection = None
        return True
    return False

def restore_selection() -> None:
    """Restores the saved selection from the data store"""
    for obj in ab_data.saved_selection:
        if ab_common.does_object_exist(obj):
            obj.select_set(True)

def does_stored_selection_exist() -> bool:
    """Returns `True` if there's a saved selection"""
    if ab_data.saved_selection:
        return True
    else:
        return False
