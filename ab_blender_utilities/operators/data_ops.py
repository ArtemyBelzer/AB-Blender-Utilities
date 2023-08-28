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
import ast
import random
import sys
from ..lib import ab_common, ab_rotation_saving


class CategoryAttributes(ab_common.Category):
    """Selection base class"""
    category = "Attributes"
    category_arg = ab_common.OperatorCategories.SELECTION
    category_icon = 'PROP_CON'

class OpABSetAttributeOnSelected(bpy.types.Operator, CategoryAttributes):
    """Sets an attribute on a selected object"""
    bl_idname = "object.ab_set_attribute_on_selected"
    bl_label = "Set Attribute On Selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    attribute_name : bpy.props.StringProperty(
        name = "Attribute Name",
        default = "",
    )

    attribute_value : bpy.props.StringProperty(
        name = "Attribute Value",
        default = "",
    )

    is_object_data : bpy.props.BoolProperty(
        name = "Set on object data instead",
        default = False,
    )

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if not self.is_object_data:
                obj[self.attribute_name] = ast.literal_eval(self.attribute_value)\
                if self.attribute_value.replace(".","").isnumeric() else self.attribute_value
                continue
            else:
                if obj.data != None:
                    obj.data[self.attribute_name] = ast.literal_eval(self.attribute_value)\
                    if self.attribute_value.replace(".","").isnumeric() else self.attribute_value

        return {'FINISHED'}
    
class OpABRandomizeAttributeOnSelected(bpy.types.Operator, CategoryAttributes):
    """Randomizes an attribute on a selected object"""
    bl_idname = "object.ab_randomize_attribute_on_selected"
    bl_label = "Randomize Attribute On Selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    attribute_name : bpy.props.StringProperty(
        name = "Attribute Name",
        default = "",
    )

    min : bpy.props.IntProperty(
        name = "Attribute Value",
        default = -1000000000,
    )

    max : bpy.props.IntProperty(
        name = "Attribute Value",
        default = 1000000000,
    )

    is_object_data : bpy.props.BoolProperty(
        name = "Set on object data instead",
        default = False,
    )

    is_float : bpy.props.BoolProperty(
        name = "Float",
        default = False,
    )

    def execute(self, context):
        random_value : int | float = random.uniform(self.min, self.max) if self.is_float else random.randrange(self.min, self.max)
        for obj in bpy.context.selected_objects:
            if not self.is_object_data:
                obj[self.attribute_name] = random_value
                continue
            else:
                if obj.data != None:
                    obj.data[self.attribute_name] = random.randrange(self.min, self.max)

        return {'FINISHED'}
    
class OpABRotationToAttribute(bpy.types.Operator, CategoryAttributes):
    """Stores/restores the rotation of the target object(s) and resets the rotation for easier editing"""
    bl_idname = "object.ab_rotation_to_attribute"
    bl_label = "Rotation to Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    store_rotation : bpy.props.BoolProperty(
        name = "Store Rotation",
        default = True
    )

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if self.store_rotation:
                ab_rotation_saving.store_rotation_in_attribute(self, obj)
            else:
                ab_rotation_saving.restore_rotation_in_attribute(obj)
                        
        return {'FINISHED'}
    
class OpABRotationToAttributeStore(bpy.types.Operator, CategoryAttributes):
    """Stores the rotation of the target object(s) and resets the rotation for easier editing"""
    bl_idname = "object.ab_rotation_as_an_attribute_store"
    bl_label = "Store Rotation as an Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.selected_objects:
                ab_rotation_saving.store_rotation_in_attribute(obj)
                        
        return {'FINISHED'}
    
class OpABRotationToAttributeRestore(bpy.types.Operator, CategoryAttributes):
    """Restores the rotation of the target object(s) and resets the rotation for easier editing"""
    bl_idname = "object.ab_rotation_as_an_attribute_restore"
    bl_label = "Restore Rotation as an Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    category_arg = ab_common.OperatorCategories.NONE

    def execute(self, context):
        for obj in bpy.context.selected_objects:
                ab_rotation_saving.restore_rotation_in_attribute(obj)
                        
        return {'FINISHED'}
    
OPERATORS : tuple[bpy.types.Operator] = (OpABSetAttributeOnSelected,
                                         OpABRandomizeAttributeOnSelected,
                                         OpABRotationToAttribute,
                                         OpABRotationToAttributeRestore,
                                         OpABRotationToAttributeStore)
