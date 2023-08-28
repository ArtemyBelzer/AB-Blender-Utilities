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
import re

def object_name_variables(obj : bpy.types.Object, value : str, index_str : str) -> str:
    # The existing name of the current object
    if "$name" in value:
        value = value.replace("$name", obj.name)
        
    # The current object type
    if "$type" in value:
        value = value.replace("$type", obj.type)

    # Is replaced by the active object name
    if "$active" in value and bpy.context.active_object is not None:
        value = value.replace("$active", bpy.context.active_object.name)

    # Adds auto numbering
    if "$index" in value:
        value = value.replace("$index", index_str)

    # Removes auto numbering from the result.
    if "$no_index" in value:
        value = value.replace("$no_index", "")

    # $replace(find, replace)
    if "$replace" in value:
        replace_strings : str = re.findall(r'\$replace\(.*?\)', value)
        for replace_str in replace_strings:
            value = value.replace(replace_str, "")

            replace_args : list[str] = replace_str.replace("$replace(", "")\
            .replace(")", "")\
            .replace(" ", "")\
            .replace("\"", "")\
            .replace("'", "")\
            .split(",")

            if len(replace_strings) != 2:
                print("Incorrect parameter")
            value = value.replace(replace_args[0], replace_args[1])
    return value
