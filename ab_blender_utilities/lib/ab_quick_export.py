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
from typing import Final

export_path_attribute : Final[str] = "ab_utilities_export_path"
export_path_warning_msg : Final[str] = "No quick export path was set in the current scene. \
Set the path using this operator: \"Extra Utilties\\File\\Set quick export path\""

def has_quick_export_path(scene : bpy.types.Scene = None) -> bool:
    """Checks if the current scene has a quick export path set.\n
    Returns `True` if the quick export attribute is found"""
    try:
        if scene:
            if scene["ab_utilities_export_path"]:
                return True
        else:
            if bpy.context.scene["ab_utilities_export_path"]:
                return True
    except:
        return False
    