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

from enum import Enum
from ..lib.color_attributes import get_col_attrib_count


class PollType(Enum):
    NONE = 0  # No check if performed with this category.
    OBJ_SEL = 1  # If the current selection is < 1, the operator is disabled.
    OBJ_MESH_SEL = 2
    VTX_COL = 3
    EDIT = 4
    CUSTOM = 5

class Category():
    """Category base class for operators"""
    category : str = ""
    category_poll : PollType = PollType.NONE
    category_icon : str = None

    @classmethod
    def poll(cl, context):
        if cl.category_poll == PollType.OBJ_SEL:
            return len(context.selected_objects) > 0
        elif cl.category_poll == PollType.OBJ_MESH_SEL:
            mesh_no = 0
            for o in context.selected_objects:
                if o.type == 'MESH':
                    mesh_no += 1
            return mesh_no > 0
        elif cl.category_poll == PollType.VTX_COL:
            return get_col_attrib_count(bpy.context.selected_objects) > 0
        elif cl.category_poll == PollType.EDIT:
            active_object = bpy.context.active_object
            if active_object == None:
                return False
            if hasattr(active_object, "mode"):
                if active_object.mode == 'EDIT':
                    return True
            return False
        return True

class CatCleanup(Category):
    """Operator category class for inheritance"""
    category = "Cleanup"
    category_icon = 'BRUSH_DATA'

class CatCleanupMat(Category):
    """Operator category class for inheritance"""
    category = "Cleanup/Materials"
    category_icon = 'MATERIAL'

class CatColorAttrib(Category):
    category = "Data/Color Attributes"
    category_poll = PollType.VTX_COL
    category_icon = 'GROUP_VCOL'

class CatCustomProperties(Category):
    category = "Data/Custom Properties"
    category_poll = PollType.OBJ_SEL
    category_icon = 'RNA'

class CatDataBlocks(Category):
    category = "Cleanup/Data Block Order"
    category_poll = PollType.OBJ_SEL
    category_icon = 'RNA'

class CatFile(Category):
    """Operator category class for inheritance"""
    category = "File"
    category_icon = 'CURRENT_FILE'

class CatFileFBX(Category):
    """Operator category class for inheritance"""
    category = "File/FBX Quick Export"
    category_poll = PollType.OBJ_SEL
    category_icon = 'FILE'

class CatFilePointCloud(Category):
    """Operator category class for inheritance"""
    category = "File/Point Cloud"
    category_icon = 'OUTLINER_DATA_POINTCLOUD'

class CatMod(Category):
    category = "Modifiers"
    category_poll = PollType.OBJ_SEL
    category_icon = 'MODIFIER'
    
class CatNaming(Category):
    category = "Naming"
    category_icon = 'GREASEPENCIL'
    
class CatObject(Category):
    category = "Objects"
    category_poll = PollType.OBJ_SEL
    category_icon = 'MESH_CUBE'
    
class CatObjectRot(Category):
    category = "Objects/Rotation"
    category_poll = PollType.OBJ_SEL
    category_icon = 'MESH_CUBE'

class CatSel(Category):
    category = "Selection"
    category_poll = PollType.OBJ_SEL
    category_icon = 'RESTRICT_SELECT_OFF'

class CatSelSaving(CatSel):
    category = "Selection/Saving"
    category_icon = 'RESTRICT_SELECT_OFF'

class CatUV(Category):
    category = "UVs"
    category_poll = PollType.OBJ_MESH_SEL
    category_icon = 'UV'
