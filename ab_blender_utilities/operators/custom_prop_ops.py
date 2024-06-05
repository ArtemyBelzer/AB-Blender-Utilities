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
from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import Operator

import re
import random
from .categories import CatCustomProperties


class ABBU_OT_RandomCustomProperty(Operator, CatCustomProperties):
    """Randomizes a custom property on a selected object"""
    bl_idname = "wm.abbu_random_custom_property"
    bl_label = "Random Custom Property"
    bl_options = {'REGISTER', 'UNDO'}

    attribute_name : StringProperty(
        name = "Attribute Name",
        default = "",
    )

    min_v : IntProperty(
        name = "Attribute Value",
        default = -1000000000,
    )

    max_v : IntProperty(
        name = "Attribute Value",
        default = 1000000000,
    )

    seed : IntProperty(
        name = "Attribute Value",
        default = 0,
    )

    is_target_data : BoolProperty(
        name = "Store property in data",
        default = False,
    )

    is_out_float : BoolProperty(
        name = "Float Output",
        default = False,
    )

    randomize_separately : BoolProperty(
        name = "Randomize the selection separately",
        default = False,
    )

    def execute(self, context):
        for i, o in enumerate(bpy.context.selected_objects):
            random.seed(self.seed + i) if self.randomize_separately else random.seed(self.seed)
            random_value : int | float = random.uniform(self.min_v, self.max_v) if self.is_out_float else random.randrange(self.min_v, self.max_v)
            if not self.is_target_data:
                o[self.attribute_name] = random_value
                continue
            else:
                if hasattr(o, "data"):
                    o.data[self.attribute_name] = random_value

        return {'FINISHED'}

class ABBU_OT_SetCustomProperty(Operator, CatCustomProperties):
    """Adds or sets a custom property"""
    bl_idname = "wm.abbu_set_custom_property"
    bl_label = "Set Custom Property"
    bl_options = {'REGISTER', 'UNDO'}
    
    prop_name : StringProperty(
        name = "Property Name",
        default = "custom_property")
    prop_val : StringProperty(
        name = "Property Value",
        default = "1.0")
    
    def _str_to_numeric_type(self, s) -> int | float:
        if s.isnumeric():
            return int(s)
        elif re.search("^[0-9]*\.[0-9]*$", s) != None:
            print(re.search("^[0-9]*\.[0-9]*$", s))
            return float(s)
        return s

    def execute(self, context):
        for o in bpy.context.selected_objects:
            custom_val = self.prop_val
            re_tp = re.search("\(.*\)", custom_val)

            if re_tp != None:
                custom_val = re.sub("\(|\)", "", custom_val).split(",")
            else:
                custom_val = self._str_to_numeric_type(custom_val)
                    
            o[self.prop_name] = custom_val
        return {'FINISHED'}

OPERATORS : tuple[Operator] = (ABBU_OT_SetCustomProperty,
                               ABBU_OT_RandomCustomProperty)
