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
from bpy.props import BoolProperty
from bpy.types import Mesh, Operator

from .categories import CatDataBlocks


def _recreate_objects_from_list(objs):
    new_objs = []
    for o in objs:
        new_o : bpy.types.Object = o.copy()
        new_o.name : str = o.name
        new_o.data : Mesh = o.data.copy()
        new_o.data.name : str = o.data.name

        if o.children:
            for child in o.children:
                child.parent = new_o
        bpy.context.collection.objects.link(new_o)
        new_objs.append(new_o)

    if bpy.app.version >= (4, 0, 0):
        for o in objs:
            bpy.data.objects.remove(o, do_unlink = True)
    else:
        bpy.ops.object.delete({"selected_objects": objs})

    return new_objs

class ABBU_OT_ReorderObjData(Operator, CatDataBlocks):
    """Reorders object data blocks alphabetically"""
    bl_idname = "wm.abbu_reorder_object_data"
    bl_label = "Reorder Object Data Alphabetically"
    bl_options = {'REGISTER', 'UNDO'}

    reverse : BoolProperty(
        name = "Reverse",
        default = False
    )

    def execute(self, context):
        sel = bpy.context.selected_objects
        objs = sorted(sel.copy(), key = lambda x : x.name, reverse = self.reverse)

        _recreate_objects_from_list(objs)
        
        return {'FINISHED'}
    
class ABBU_OT_ReorderObjDataMod(Operator, CatDataBlocks):
    """Reorders object data blocks alphabetically based on the modifier order"""
    bl_idname = "wm.abbu_reorder_obj_data_mod"
    bl_label = "Reorder Object Data Alphabetically Based On Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sel = bpy.context.selected_objects
        objs = []
        mod_refs = []
        
        for o in sel:
            if hasattr(o, "modifiers"):
                for modifier in o.modifiers:
                    if hasattr(modifier, "object"):
                        if modifier.object not in objs:
                            objs.append(modifier.object)
                            mod_refs.append(modifier)
                            
        for mod, o in zip(mod_refs, _recreate_objects_from_list(objs)):
            mod.object = o
        
        return {'FINISHED'}
    
OPERATORS : tuple[Operator] = (ABBU_OT_ReorderObjData,
                               ABBU_OT_ReorderObjDataMod)
