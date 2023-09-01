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
import operator
from typing import Final
from . import ab_constants, ab_persistent
from ..operators import color_attribute_ops, data_ops, uv_ops
from bl_ui import properties_data_mesh, properties_object

__init : bool = False

class OBJECT_PT_ab_attributes(properties_object.ObjectButtonsPanel,
                                         bpy.types.Panel):
    """Attributes panel for mesh object"""
    bl_idname = "OBJECT_PT_ab_attributes"
    bl_label = "Attribute Utilities"
    children = list = []
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'BLENDER_WORKBENCH_NEXT'}
    icon = None

    @classmethod
    def poll(cls, context) -> bool:
        prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()
        return prefs.show_object_attribute_utils_in_properties and prefs.utilties_in_properties

    def draw(self : any, context: any) -> None:
        layout = self.layout
        layout.operator(data_ops.OpABSetAttributeProperties.bl_idname, text = "Set", icon = 'GREASEPENCIL')
        layout.operator(data_ops.OpABRandomizeAttributeProperties.bl_idname, text = "Randomize", icon = 'PARTICLE_DATA')

class DATA_PT_ab_attributes(properties_data_mesh.MeshButtonsPanel,
                                         bpy.types.Panel):
    """Attributes panel for mesh data"""
    bl_idname = "DATA_PT_ab_attributes"
    bl_label = "Attribute Utilities"
    children = list = []
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'BLENDER_WORKBENCH_NEXT'}
    icon = None

    @classmethod
    def poll(cls, context) -> bool:
        prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()
        return prefs.show_object_attribute_utils_in_properties and prefs.utilties_in_properties

    def draw(self : any, context: any) -> None:
        layout = self.layout
        layout.operator(data_ops.OpABSetAttributePropertiesData.bl_idname, text = "Set", icon = 'GREASEPENCIL')
        layout.operator(data_ops.OpABRandomizeAttributePropertiesData.bl_idname, text = "Randomize", icon = 'PARTICLE_DATA')

class DATA_PT_ab_colors(properties_data_mesh.MeshButtonsPanel,
                                         bpy.types.Panel):
    """Attributes panel for mesh data"""
    bl_idname = "DATA_PT_ab_colors"
    bl_label = "Color Attribute Utilities"
    children = list = []
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'BLENDER_WORKBENCH_NEXT'}
    icon = None

    @classmethod
    def poll(cls, context) -> bool:
        prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()
        return prefs.show_object_attribute_utils_in_properties and prefs.utilties_in_properties

    def draw(self : any, context: any) -> None:
        layout = self.layout
        layout.operator(color_attribute_ops.OpABDeleteColorAttributes.bl_idname, text = "Select & Delete", icon = 'X')
        layout.operator(color_attribute_ops.OpABRenameColorAttribute.bl_idname, text = "Rename", icon = 'GREASEPENCIL')
        layout.operator(color_attribute_ops.OpABSetActiveColorAttribute.bl_idname, text = "Set Active", icon = 'CHECKBOX_HLT')
        layout.operator(color_attribute_ops.OpABColorAttributeRenderSet.bl_idname, text = "Set Render", icon = 'RESTRICT_RENDER_OFF')
        layout.operator(color_attribute_ops.OpABRemoveVertexColorsFromSelected.bl_idname, text = "Remove All", icon = 'TRASH')

class DATA_PT_ab_uv_utilities(properties_data_mesh.MeshButtonsPanel,
                                         bpy.types.Panel):
    """Attributes panel for mesh data"""
    bl_idname = "DATA_PT_ab_uv_utilities"
    bl_label = "UV Map Utilities"
    children = list = []
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'BLENDER_WORKBENCH_NEXT'}
    icon = None

    @classmethod
    def poll(cls, context) -> bool:
        prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()
        return prefs.show_object_attribute_utils_in_properties and prefs.utilties_in_properties

    def draw(self : any, context: any) -> None:
        layout = self.layout
        layout.operator(uv_ops.OpABAddUVChannel.bl_idname, text = "Add", icon = 'ADD')
        layout.operator(uv_ops.OpABDeleteUVChannel.bl_idname, text = "Select & Delete", icon = 'X')
        layout.operator(uv_ops.OpABRenameUVChannel.bl_idname, text = "Rename", icon = 'GREASEPENCIL')
        layout.operator(uv_ops.OpABSetActiveUVChannel.bl_idname, text = "Set Active", icon = 'CHECKBOX_HLT')
        

def __panel_poll(cls, context) -> bool:
    return getattr(ab_persistent.get_preferences(), f"panel_{cls.internal_name}_show")

def panel_draw(self : any, context: any) -> None:
    """Shared panel function"""
    panel_ops : list[bpy.types.Operator] = [cls for cls in self.children if issubclass(cls, bpy.types.Operator)]
    layout = self.layout
    
    displayed_ops : int = 0
    for panel_op in panel_ops:
        # Operator display
        if hasattr(panel_op, "poll"):  # Does the operator have a "poll" function?
            if panel_op.poll(context):
                layout.operator(panel_op.bl_idname)
                displayed_ops += 1
            else:
                layout.operator(panel_op.bl_idname)
        else:
            layout.operator(panel_op.bl_idname)
            displayed_ops += 1

__dynamic_panel_categories : set = set({})  # Variable used by dynamic panel creation to keep track of the amount of panels generated.
__dynamic_panels : list = []
__panels : tuple = (OBJECT_PT_ab_attributes,
                    DATA_PT_ab_attributes,
                    DATA_PT_ab_colors,
                    DATA_PT_ab_uv_utilities)

def __does_dynamic_panel_exist(category : str = "Example/Category") -> bool:
    if category in __dynamic_panel_categories:
        return True
    return False

def create_dynamic_panel_class(category : str = "Example/Category",
                                 classes : list = []) -> tuple[bpy.types.Panel]:
    global __dynamic_panel_categories, __dynamic_panels
    if category in __dynamic_panel_categories:
        return None
    category_split : list[str] = category.split("/")

    __dynamic_panel_categories.add(category)

    icon : str = 'COLLAPSEMENU'

    menu_name : str = category_split[-1:][0]
    internal_name : str = menu_name.lower().replace(" ", "_").replace("/", "_")
    

    children : list[any] = []  # Operators and submenus that have the category value of the current menu.
    for cls in classes:
        if hasattr(cls, "category"):
            if cls.category == category:
                children.append(cls)
                if cls.category_icon != None:
                    icon = cls.category_icon

    dynamic_cls = type(f"VIEW3D_PT_{ab_constants.plugin_name_internal}_panel_{internal_name}".format(),
                            (bpy.types.Panel,),
                            {

                                "bl_idname" : f"VIEW3D_PT_{ab_constants.plugin_name_internal}_panel_{internal_name}",
                                "bl_label" : menu_name,
                                "bl_category" : ab_constants.plugin_name_short,
                                "bl_space_type" : 'VIEW_3D',
                                "bl_region_type" : 'UI',

                                "internal_name" : internal_name,
                                "children" : children,
                                "category" : category,
                                "is_pie" : False,
                                "icon" : icon,

                                "draw" : lambda self, context : panel_draw(self, context),
                                "poll" : classmethod(__panel_poll)
                            }
                         )
    
    if dynamic_cls not in __dynamic_panels:
        __dynamic_panels.append(dynamic_cls)

    return dynamic_cls

def __load(classes : list[bpy.types.Operator, bpy.types.Panel]) \
-> list[bpy.types.Panel]:
    global __init, __dynamic_panels
    if not __init:
        if classes is None:
            ValueError(f"{ab_constants.input_classes_none}")
        
        panels : list[bpy.types.Panel] = list(__panels)

        # Sorts classes by their "bl_idname"
        classes.sort(key = operator.attrgetter("bl_label"))
        
        # Filters classes in case there are other types.
        op_classes : list[bpy.types.Operator] = [op for op in classes if issubclass(op, bpy.types.Operator)\
                                                 and hasattr(op, "category")]
        
        # Unique menu set
        panel_set : set[bpy.types.Panel] = set({})

        # The menu structure is created here.
        for op_class in op_classes:
            # Example category = "Menu1/Menu2"
            if hasattr(op_class, "category"):
                panel_set.add(op_class.category)

        # dynamic_menus : list[tuple] = []
        for panel in panel_set:
            create_dynamic_panel_class(category = panel, classes = op_classes)

        __dynamic_panels.sort(key = operator.attrgetter("bl_label"))

        panels += __dynamic_panels

        __init = True
        return panels
    else:
        RuntimeError(f"{ab_constants.menu_initialized}")

def load(classes : list[bpy.types.Operator, bpy.types.Panel]) \
-> list[bpy.types.Panel]:
    """Initializes operator panels.\n
    Returns a list of the newly generated panel classes."""
    panels : list[bpy.type.Panel] = []
    try:
        panels =  __load(classes)
    except Exception as e:
        print(f"{ab_constants.error}{e}")
    finally:
        return panels

def unload() -> None:
    global __init
    try:
        if __init:
            __init = False
        else:
            RuntimeError(f"{ab_constants.error}{ab_constants.menu_not_initialized}")
    finally:
        return None