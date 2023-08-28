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

"""
Contains persistent methods used to manage the addon and its preferences.
"""
import bpy
from bpy.app.handlers import persistent

@persistent
def get_preferences() -> bpy.types.AddonPreferences:
    """Returns `bpy.types.AddonPreferences` (preferences) of the current package."""
    return bpy.context.preferences.addons[__package__[:len(__package__)-6]].preferences

@persistent
def load_settings(self, context) -> None:
    prefs : bpy.types.AddonPreferences = get_preferences()

def load() -> None:
    bpy.app.handlers.load_post.append(load_settings)

def unload() -> None:
    bpy.app.handlers.load_post.remove(load_settings)
