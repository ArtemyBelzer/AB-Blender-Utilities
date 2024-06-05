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
from bpy.types import Operator

from .categories import CatMod
from ..lib import common, mod_cache
from ..lib.mod_cache import cached_obj_prop_name, parent_and_keep_transform


class ABBU_OT_CacheModifiers(Operator, CatMod):
    """Caches the modifiers of the currently selected object by duplicating it, applying modifiers on the duplicate, and hiding the original object with disabled modifiers"""
    bl_idname = "wm.abbu_cache_modifiers"
    bl_label = "Cache Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects_ordered : tuple[bpy.types.Object] = tuple(sorted(bpy.context.selected_objects,
                                                                          key = lambda x: x.name,
                                                                          reverse=False))

        for src_obj in selected_objects_ordered:

            deps_graph = bpy.context.evaluated_depsgraph_get()
            obj_data_new = bpy.data.meshes.new_from_object(src_obj.evaluated_get(deps_graph), depsgraph = deps_graph)
            

            copied_obj : bpy.types.Object = bpy.data.objects.new(src_obj.name, obj_data_new)
            copied_obj.matrix_world = src_obj.matrix_world

            copied_obj.name = src_obj.name
            copied_obj.data.name = src_obj.data.name
            
            # Rename source object
            src_obj.name = copied_obj.name + "_cache"
            src_obj.data.name = copied_obj.data.name + "_cache"

            # Disable modifiers on source object
            for modifier in src_obj.modifiers:
                modifier.show_viewport = False

            for child in src_obj.children:
                parent_and_keep_transform(copied_obj, child)
            
            bpy.context.collection.objects.link(copied_obj)

            copied_obj[cached_obj_prop_name] : bpy.types.Object = src_obj
            src_obj.select_set(False)
            copied_obj.select_set(True)

            if bpy.context.active_object == src_obj:
                bpy.context.view_layer.objects.active = copied_obj

            src_obj.hide_viewport = True
            src_obj.hide_render = True

        return {'FINISHED'}

class ABBU_OT_SelectModifierObjects(Operator, CatMod):
    """Selects the objects referenced inside modifiers on one or more objects"""
    bl_idname = "object.abbu_select_modifier_objects"
    bl_label = "Select Modifier Objects"
    bl_options = {'REGISTER', 'UNDO'}

    deselect_current : BoolProperty(
        name = "Deselect Current",
        default = False
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            common.get_modifier_objects(o, select=True)

            if self.deselect_current:
                o.select_set(False)
                        
        return {'FINISHED'}

class ABBU_OT_SetModifierVis(Operator, CatMod):
    """Sets the viewport visibility of objects referenced inside modifiers on one or more selected objects"""
    bl_idname = "object.abbu_set_modifier_object_viewport_vis"
    bl_label = "Set Modifier Object(s) Viewport Visibility"
    bl_options = {'REGISTER', 'UNDO'}

    visible : BoolProperty(
        default = False
    )

    def execute(self, context):
        for o in bpy.context.selected_objects:
            cached_objects : tuple[bpy.types.Object] = mod_cache.get_linked_cached_objects(o)
            for cached_object in cached_objects:
                modifier_objects : tuple[bpy.types.Object] = common.get_modifier_objects(cached_object)
                for modifier_obj in modifier_objects:
                    modifier_obj.hide_viewport = not self.visible

            modifier_objects : tuple[bpy.types.Object] = common.get_modifier_objects(o)
            for modifier_obj in modifier_objects:
                modifier_obj.hide_viewport = not self.visible
                        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        box = col.box()
        row = box.row()
        row.label(text = "Viewport Object Visibility:")
        row.prop(self, 'visible', icon = 'RESTRICT_VIEW_OFF' if self.visible else 'RESTRICT_VIEW_ON',
                 text = 'Visible' if self.visible else 'Hidden')

class ABBU_OT_UncacheModifiers(Operator, CatMod):
    """Restores the original mesh with its modifiers prior to caching"""
    bl_idname = "wm.abbu_uncache_modifiers"
    bl_label = "Uncache Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects_ordered : tuple[bpy.types.Object] = tuple(sorted(bpy.context.selected_objects,
                                                                          key = lambda x: x.name,
                                                                          reverse=False))

        objects_to_delete : list[bpy.types.Object] = []
        for o in selected_objects_ordered:
            if cached_obj_prop_name in o:
                cached_obj : bpy.types.Object = o[cached_obj_prop_name]
                cached_obj.name = o.name
                cached_obj.data.name = o.data.name

                for modifier in cached_obj.modifiers:
                    modifier.show_viewport = True

                cached_obj.hide_viewport = o.hide_viewport
                cached_obj.hide_render = o.hide_render

                cached_obj.select_set(True)

                for child in o.children:
                    parent_and_keep_transform(cached_obj, child)

                if bpy.context.active_object == o:
                    bpy.context.view_layer.objects.active = cached_obj

                objects_to_delete.append(o)

        if bpy.app.version >= (4, 0, 0):
            for o in objects_to_delete:
                bpy.data.objects.remove(o, do_unlink = True)
        else:
            bpy.ops.object.delete({"selected_objects": objects_to_delete})

        return {'FINISHED'}

OPERATORS : tuple[Operator] = (ABBU_OT_SelectModifierObjects,
                               ABBU_OT_SetModifierVis,
                               ABBU_OT_CacheModifiers,
                               ABBU_OT_UncacheModifiers)
