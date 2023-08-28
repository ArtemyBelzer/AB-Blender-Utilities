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
import os
import sys
from ..lib import ab_json
from types import ModuleType

def _load_modules_from_file() -> tuple[ModuleType]:
    modules : list[ModuleType] = []
    
    addon_dir = bpy.utils.user_resource('SCRIPTS', path = "addons")
    operator_dir = os.path.join(addon_dir, __package__.replace(".", "\\"))
    operator_file_path = os.path.join(operator_dir, "operators.json")

    with open(operator_file_path, 'r') as file_handle:
           module_strings : tuple[str] = ab_json.parse_module_file_data(file_handle.read())
           for module in module_strings:
                module_path : str = module[:-3].replace("\\", ".")
                module_paths : list = module[:-3].replace("\\", ".").split(".")
                module_name : str = module_paths[-1:][0]

                if len(module_paths) > 1:
                     exec(f"from .{''.join(module_paths[:-1])} import {module_name}")
                else:
                    exec(f"from . import {module_name}")

                imported_module : ModuleType = sys.modules[f"{__package__}.{module_path}"]
                modules.append(imported_module)
                    
    return tuple(modules)

def get_modules() -> tuple[ModuleType]:
    modules : tuple[ModuleType] = _load_modules_from_file()
    return modules
