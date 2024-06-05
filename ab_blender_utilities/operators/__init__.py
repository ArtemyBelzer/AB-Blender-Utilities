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

from . import color_attribute_ops, custom_prop_ops, global_ops, mat_ops, modifier_ops, naming_ops, rot_ops, data_block_ops, selection_ops, uv_ops
from .file_ops import file_ops_common, file_ops_custom, file_ops_fbx
from types import ModuleType


def get_modules() -> tuple[ModuleType]:
    modules : tuple[ModuleType] = (color_attribute_ops,
                                   custom_prop_ops,
                                   global_ops,
                                   mat_ops,
                                   modifier_ops,
                                   naming_ops,
                                   rot_ops,
                                   data_block_ops,
                                   selection_ops,
                                   uv_ops,
                                   file_ops_common,
                                   file_ops_custom,
                                   file_ops_fbx)
    return modules
