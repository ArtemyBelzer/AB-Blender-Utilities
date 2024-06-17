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

bl_info = {
    "name" : "Artemy Belzer's Blender Utilities",
    "blender" : (4, 0, 0),
    "author" : "Artemy belzer",
    "location" : "3D Viewport panels, the addon's pie menu (default keymap `Alt + E`), the Object menu, or the Object context menu.",
    "category" : "Utility",
    "version" : (1, 3, 1)
}

if "core" in locals():
    import importlib
    importlib.reload(core)
else:
    from .addon import core

def register() -> None:
    core.register()

def unregister() -> None:
    core.unregister()
