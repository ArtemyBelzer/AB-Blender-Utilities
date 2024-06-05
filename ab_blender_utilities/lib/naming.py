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
import re

from typing import Final


__exp_pattern : Final[str] = r'\$\w+\([^)]*\)'
__exp_name : Final[str] = r'\$name\(\)'
__exp_type : Final[str] = r'\$type\(\)'
__exp_active : Final[str] = r'\$active\(\)'
__exp_idx : Final[str] = r'\$idx\((.*?)\)'
__exp_oidx : Final[str] = r'\$oidx\((.*?)\)'
__exp_replace : Final[str] = r'\$replace\((.*?)\)'
__pattern_brackets : Final[str] = r'\((.*?)\)'
__pattern_replace_arg : Final[str] = r'\$replace\(\"([^"]+)\",\"([^"]+)\"\)'

def object_name_custom_expr(o : bpy.types.Object, value : str, index_str : str) -> str | bool:
    expression_find = re.finditer(__exp_pattern, value)
    oidx_found : bool = False
    expressions = []
    for exp in expression_find:
        expressions.append(value[exp.start():exp.end()])
    for exp in expressions:
        target_exp = re.escape(exp)
        expression_match = re.search(target_exp, value)
        # The existing name of the current object
        if bool(re.search(__exp_name, value)):
            value = value[:expression_match.start()] + o.name + value[expression_match.end():]
        # Object type
        elif bool(re.search(__exp_type, value)):
            value = value[:expression_match.start()] + o.type + value[expression_match.end():]
        # Active object
        elif bool(re.search(__exp_active, value)):
            if bpy.context.active_object == None:
                continue
            value = value[:expression_match.start()] + bpy.context.active_object.name + value[expression_match.end():]
        # Index
        elif bool(re.search(__exp_idx, value)):
            padding = re.findall(__pattern_brackets, exp)[0]
            index = index_str
            if padding != '':
                if padding.isnumeric():
                    index = index.zfill(int(padding))
            value = value[:expression_match.start()] + index + value[expression_match.end():]
        # Index override
        elif bool(re.search(__exp_oidx, value)):
            oidx_found = True
        # Replace words
        elif bool(re.search(__exp_replace, value)):
            words = re.findall(__pattern_replace_arg, exp.strip(" "))[0]
            value = value[:expression_match.start()] + value[expression_match.end():]
            value = value.replace(words[0], words[1])

    return value, oidx_found
