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

from types import ModuleType

from . import cleanup_ops, color_attribute_ops, data_ops, global_ops, modifier_ops, naming_ops, obj_ops, selection_ops, uv_ops
from .file_ops import file_ops_common, file_ops_custom, file_ops_fbx

__modules : tuple[ModuleType] = (cleanup_ops,
                                 color_attribute_ops,
                                 data_ops,
                                 global_ops,
                                 modifier_ops,
                                 naming_ops,
                                 obj_ops,
                                 selection_ops,
                                 uv_ops,
                                 file_ops_common,
                                 file_ops_custom,
                                 file_ops_fbx)

def get_modules() -> tuple[ModuleType]:
    return __modules
