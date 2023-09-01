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
from ..lib import ab_common, ab_modifier_caching

class CategoryBaseModifier(ab_common.Category):
    category = "Modifiers"
    category_arg = ab_common.OperatorCategories.SELECTION
    category_icon = 'MODIFIER'

class OpABSelectModifierObjects(bpy.types.Operator, CategoryBaseModifier):
    """Selects the objects referenced inside modifiers"""
    bl_idname = "object.ab_select_modifier_objects"
    bl_label = "Select Modifier Objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    deselect_current : bpy.props.BoolProperty(
        name = "Deselect Current",
        default = False
    )

    def execute(self, context):
        for obj in ab_common.get_selected_objects():
            ab_common.get_modifier_objects(obj, select=True)

            if self.deselect_current:
                obj.select_set(False)
                        
        return {'FINISHED'}
    
class OpABSetModifierObjectViewportVisibility(bpy.types.Operator, CategoryBaseModifier):
    """Sets the viewport visiblity of the objects referenced inside modifiers"""
    bl_idname = "object.ab_set_modifier_object_viewport_visibility"
    bl_label = "Set modifier object viewport visibility"
    bl_options = {'REGISTER', 'UNDO'}
    
    visible : bpy.props.BoolProperty(
        default = False
    )

    def execute(self, context):
        for obj in ab_common.get_selected_objects():
            cached_objects : tuple[bpy.types.Object] = ab_modifier_caching.get_linked_cached_objects(obj)
            for cached_object in cached_objects:
                modifier_objects : tuple[bpy.types.Object] = ab_common.get_modifier_objects(cached_object)
                for modifier_obj in modifier_objects:
                    modifier_obj.hide_viewport = not self.visible

            modifier_objects : tuple[bpy.types.Object] = ab_common.get_modifier_objects(obj)
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
    
class OpABCacheModifiers(bpy.types.Operator, CategoryBaseModifier):
    """Caches the modifiers of the currently selected"""
    bl_idname = "wm.ab_cache_modifiers"
    bl_label = "Cache Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects_ordered : tuple[bpy.types.Object] = tuple(sorted(ab_common.get_selected_objects(),
                                                                          key = lambda x: x.name,
                                                                          reverse=False))

        for current_obj in selected_objects_ordered:
            # Create a new mesh
            # if current_obj.type == 'MESH':
            deps_graph = bpy.context.evaluated_depsgraph_get()
            obj_data_new = bpy.data.meshes.new_from_object(current_obj.evaluated_get(deps_graph),
                                                            depsgraph = deps_graph)
            copied_obj_name : str = current_obj.name
            copied_obj : bpy.types.Object = bpy.data.objects.new(current_obj.name, obj_data_new)
            copied_obj.matrix_world = current_obj.matrix_world
            copied_obj.name = copied_obj_name

            copied_obj_data_name : str = current_obj.data.name
            copied_obj.data.name = copied_obj_data_name
            
            # Source  object name
            current_obj.name = f"{copied_obj.name}_cache"
            current_obj.data.name = f"{copied_obj.data.name}_cache"


            # stored_modifiers : list [bpy.types.Modifier] = []
            for modifier in current_obj.modifiers:
                # stored_modifiers.append(modifier)
                modifier.show_viewport = False
            # current_obj.modifiers.clear()

            # print(f"Copied modifiers = {stored_modifiers}")

            # Re-parent children
            if current_obj.children:
                for child in current_obj.children:
                    child.parent = copied_obj
            
            # Link object to scene
            bpy.context.collection.objects.link(copied_obj)

            copied_obj["ab_cached_object"] : bpy.types.Object = current_obj
            current_obj.select_set(False)
            copied_obj.select_set(True)

            if bpy.context.active_object == current_obj:
                bpy.context.view_layer.objects.active = copied_obj

            current_obj.hide_viewport = True
            current_obj.hide_render = True

            

            # copied_obj["ab_cached_modifiers"] : list[bpy.types.Modifier] = stored_modifiers
        
        # bpy.ops.object.delete({"selected_objects": selected_objects})
        
        return {'FINISHED'}
    
class OpABUnCacheModifiers(bpy.types.Operator, CategoryBaseModifier):
    """Returns cached modifiers from the object"""
    bl_idname = "wm.ab_uncache_modifiers"
    bl_label = "Uncache Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects_ordered : tuple[bpy.types.Object] = tuple(sorted(ab_common.get_selected_objects(),
                                                                          key = lambda x: x.name,
                                                                          reverse=False))

        objects_to_delete : list[bpy.types.Object] = []
        for current_obj in selected_objects_ordered:
            if current_obj["ab_cached_object"]:
                cached_obj : bpy.types.Object = current_obj["ab_cached_object"]
                cached_obj.name = current_obj.name
                cached_obj.data.name = current_obj.data.name

                for modifier in cached_obj.modifiers:
                    modifier.show_viewport = True

                cached_obj.hide_viewport = current_obj.hide_viewport
                cached_obj.hide_render = current_obj.hide_render

                objects_to_delete.append(current_obj)

                cached_obj.select_set(True)

                if bpy.context.active_object == current_obj:
                    bpy.context.view_layer.objects.active = cached_obj

        bpy.ops.object.delete({"selected_objects": objects_to_delete})
        
        return {'FINISHED'}

OPERATORS : tuple[bpy.types.Operator] = (OpABSelectModifierObjects,
                                         OpABSetModifierObjectViewportVisibility,
                                         OpABCacheModifiers,
                                         OpABUnCacheModifiers)
