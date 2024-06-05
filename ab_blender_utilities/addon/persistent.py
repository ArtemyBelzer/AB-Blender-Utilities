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
Contains persistent methods used to manage the addon and its preferences.
"""
import bpy
from bpy.types import AddonPreferences
from bpy.app.handlers import persistent


@persistent
def get_preferences() -> AddonPreferences:
    """Returns `AddonPreferences` (preferences) of the current package."""
    return bpy.context.preferences.addons[__package__[:len(__package__)-6]].preferences
