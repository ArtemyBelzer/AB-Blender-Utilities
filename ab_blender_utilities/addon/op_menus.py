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
from bpy.types import Menu, Operator, Panel

from typing import Final
from . import constants
from .persistent import get_preferences
from ..operators.categories import CatCleanup, CatCleanupMat, CatColorAttrib, CatCustomProperties, CatDataBlocks, CatFile, CatFileFBX, CatFilePointCloud, CatMod, CatNaming, CatObject, CatObjectRot, CatSel, CatSelSaving, CatUV

def _expand_menu(layout, menu) -> None:
    box = layout.box()
    box.label(text = menu.bl_label, icon = menu.icon)
    for key, submenu in menu.menus.items():
        _expand_menu(box, submenu)
    for op in menu.operators:
        box.operator(op.bl_idname)

class ABBU_MT_Menu(Menu):
    bl_idname = "AABU_MT_Menu"
    bl_label = "Menu"
    category = "Category"
    expanded = False
    icon = 'NONE'
    is_pie = False
    menus = dict()
    operators = []
    
    def draw(self, context):
        layout = self.layout
        if self.is_pie:
            layout = self.layout.menu_pie()
        for key, menu in self.menus.items():
            if menu.expanded and self.is_pie:
                _expand_menu(layout, menu)
            else:
                layout.menu(menu.bl_idname, icon = menu.icon)

        for op in self.operators:
            layout.operator(op.bl_idname)

class ABBU_MT_CleanupMat(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_CleanupMat"
    bl_label = "Materials"
    category = CatCleanupMat.category
    icon = CatCleanupMat.category_icon
    operators = []

class ABBU_MT_CleanupDataBlocks(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_CleanupDataBlocks"
    bl_label = "Data Blocks"
    category = CatDataBlocks.category
    icon = CatDataBlocks.category_icon
    operators = []

class ABBU_MT_Cleanup(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_Cleanup"
    bl_label = "Cleanup"
    category = CatCleanup.category
    icon = CatCleanup.category_icon
    menus = {ABBU_MT_CleanupDataBlocks.category : ABBU_MT_CleanupDataBlocks,
             ABBU_MT_CleanupMat.category : ABBU_MT_CleanupMat}
    operators = []

class ABBU_MT_DataCustomProperties(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_DataCustomProperties"
    bl_label = "Custom Properties"
    category = CatCustomProperties.category
    icon = CatCustomProperties.category_icon
    operators = []

class ABBU_MT_DataColorAttrib(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_DataColorAttrib"
    bl_label = "Color Attributes"
    category = CatColorAttrib.category
    icon = CatColorAttrib.category_icon
    operators = []

class ABBU_MT_Data(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_Data"
    bl_label = "Data"
    category = "Data"
    icon = CatCustomProperties.category_icon
    menus = {ABBU_MT_DataColorAttrib.category : ABBU_MT_DataColorAttrib,
             ABBU_MT_DataCustomProperties.category : ABBU_MT_DataCustomProperties}
    operators = []

class ABBU_MT_FilePointCloud(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_FilePointCloud"
    bl_label = "Point Cloud"
    category = CatFilePointCloud.category
    icon = CatFilePointCloud.category_icon
    operators = []

class ABBU_MT_FileFBX(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_FileFBX"
    bl_label = "FBX"
    category = CatFileFBX.category
    icon = CatFileFBX.category_icon
    operators = []

class ABBU_MT_File(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_File"
    bl_label = "File"
    category = CatFile.category
    expanded = True
    icon = CatFile.category_icon
    menus = {ABBU_MT_FileFBX.category : ABBU_MT_FileFBX,
             ABBU_MT_FilePointCloud.category : ABBU_MT_FilePointCloud}
    operators = []

class ABBU_MT_Modifiers(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_Modifiers"
    bl_label = "Modifiers"
    category = CatMod.category
    icon = CatMod.category_icon
    operators = []

class ABBU_MT_Naming(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_Naming"
    bl_label = "Naming"
    category = CatNaming.category
    icon = CatNaming.category_icon
    operators = []

class ABBU_MT_ObjectsRot(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_ObjectsRot"
    bl_label = "Rotation"
    category = CatObjectRot.category
    icon = CatObjectRot.category_icon
    operators = []

class ABBU_MT_Objects(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_Objects"
    bl_label = "Objects"
    category = CatObject.category
    icon = CatObject.category_icon
    menus = {ABBU_MT_ObjectsRot.category : ABBU_MT_ObjectsRot}
    operators = []

class ABBU_MT_SelectionSaving(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_SelectionSaving"
    bl_label = "Saving"
    category = CatSelSaving.category
    icon = CatSelSaving.category_icon
    operators = []

class ABBU_MT_Selection(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_Selection"
    bl_label = "Selection"
    category = CatSel.category
    icon = CatSel.category_icon
    menus = {ABBU_MT_SelectionSaving.category : ABBU_MT_SelectionSaving}
    operators = []

class ABBU_MT_UVs(ABBU_MT_Menu):
    bl_idname = "ABBU_MT_UVs"
    bl_label = "UVs"
    category = CatUV.category
    icon = CatUV.category_icon
    operators = []

_menu_children = {ABBU_MT_Cleanup.category : ABBU_MT_Cleanup,
                  ABBU_MT_Data.category : ABBU_MT_Data,
                  ABBU_MT_File.category : ABBU_MT_File,
                  ABBU_MT_Modifiers.category : ABBU_MT_Modifiers,
                  ABBU_MT_Naming.category : ABBU_MT_Naming,
                  ABBU_MT_Objects.category : ABBU_MT_Objects,
                  ABBU_MT_Selection.category : ABBU_MT_Selection,
                  ABBU_MT_UVs.category : ABBU_MT_UVs}

__menu_children_submenus = {ABBU_MT_CleanupDataBlocks.category : ABBU_MT_CleanupDataBlocks,
                            ABBU_MT_CleanupMat.category : ABBU_MT_CleanupMat,
                            ABBU_MT_DataColorAttrib.category : ABBU_MT_DataColorAttrib,
                            ABBU_MT_DataCustomProperties.category : ABBU_MT_DataCustomProperties,
                            ABBU_MT_FileFBX.category : ABBU_MT_FileFBX,
                            ABBU_MT_FilePointCloud.category : ABBU_MT_FilePointCloud,
                            ABBU_MT_ObjectsRot.category : ABBU_MT_ObjectsRot,
                            ABBU_MT_SelectionSaving.category : ABBU_MT_SelectionSaving}

class ABBU_MT_Utility_Menu(ABBU_MT_Menu):
    """Main operator menu of the Blender Utility addon"""
    bl_idname = "AABU_MT_Utility_Menu"
    bl_label = constants.plugin_menu_name
    is_pie = False
    menus = _menu_children

class ABBU_MT_Utility_Menu_Pie(ABBU_MT_Menu):
    """Main pie operator menu of Blender Utility addon"""
    bl_idname = "AABU_MT_Utility_Menu_Pie"
    bl_label = constants.plugin_menu_name + " Menu"
    is_pie = True
    menus = _menu_children

    def draw(self, context):
        super().draw(context)

def menu_func(self : any, context : any) -> None:
    """This function is for the base operator menu in other menus."""
    layout = self.layout
    layout.separator()
    layout.menu(ABBU_MT_Utility_Menu.bl_idname)

__menu : Final[tuple[Menu]] = (ABBU_MT_Utility_Menu,
                               ABBU_MT_Utility_Menu_Pie)

__menu_registration_order = []

def load(classes : list[Operator | Panel]):
    global __menu_registration_order
    __menu_registration_order.clear()
    for menu in __menu:
        bpy.utils.register_class(menu)
        __menu_registration_order.append(menu)

    menus = dict(**_menu_children, **__menu_children_submenus)

    for key, menu in menus.items():
        bpy.utils.register_class(menu)
        __menu_registration_order.append(menu)

    for cl in classes:
        if cl.category in menus:
            menus[cl.category].operators.append(cl)

    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

def unload() -> None:
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)

    for menu in reversed(__menu_registration_order):
        bpy.utils.unregister_class(menu)
        menu.operators.clear()
