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
from ..lib import ab_common
from . import ab_constants, ab_persistent

__init : bool = False

def __pie_menu_display_name() -> str:
    prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()

    return " Pie" if prefs.alternative_menu else ""
    

def __menu_has_prefs(menu : bpy.types.Menu) -> bool:
    """Returns `True` if the addon preferences have the attributes to
    hide the submenu entry or draw it as buttons."""
    prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()

    return hasattr(prefs, f"submenu_{menu.internal_name}_show") and\
           hasattr(prefs, f"submenu_{menu.internal_name}_buttons")

def __menu_layout(layout : bpy.types.UILayout,
                  menu : bpy.types.Menu,
                  is_pie : bool,
                  *,
                  as_buttons : bool = False,
                  initial : bool = False) -> None:
    """Adds a `bpy.types.Menu` object to a `bpy.types.UILayout`.\n
    Draws the menu with an icon if it belongs to a pie menu.\n
    The `as_buttons` argument draws the operators contained within a `menu` and its child submenus as buttons."""
    prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()

    if as_buttons and is_pie:
        if initial and not prefs.alternative_menu:
            column = layout.column()
            spacing = column.column()
            spacing.separator()
            spacing.scale_x = prefs.pie_menu_button_spacing_x
            spacing.scale_y = prefs.pie_menu_button_spacing_y
            layout = column

        box = layout.box()

        for cls in menu.children:
            if issubclass(cls, bpy.types.Operator):
                if getattr(prefs, f"submenu_{menu.internal_name}_show"):  # Skip adding operators if the menu shouldn't be shown.
                    box.operator(cls.bl_idname)
            elif issubclass(cls, bpy.types.Menu):
                """
                A submenu can be rendered as buttons only when an attribute is present in the preferences of the addon.
                It's safer to perform a check using `__menu_has_prefs` before calling this function.
                """
                if getattr(prefs, f"submenu_{cls.internal_name}_show"):
                    __menu_layout(box, cls, is_pie, as_buttons = as_buttons)  # Render submenu buttons
    else:
        layout.menu(menu.bl_idname, icon = menu.icon) \
        if is_pie else layout.menu(menu.bl_idname)

# Base menu draw function

def menu_draw(self : any, context: any, *, is_pie : bool = False) -> None:
    """Shared menu function"""
    prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()
    menu_submenus : list[bpy.types.Menu] = [cls for cls in self.children if issubclass(cls, bpy.types.Menu)]
    menu_ops : list[bpy.types.Operator] = [cls for cls in self.children if issubclass(cls, bpy.types.Operator)]
    layout = self.layout
    if is_pie:
        if prefs.alternative_menu:
            layout = layout.menu_pie()
            layout = layout.column()
            layout.scale_y = 2
            layout.scale_x = 2
            layout = layout.box()
        else:
            layout = layout.menu_pie()

    for submenu_i in menu_submenus:
        try:
            if __menu_has_prefs(submenu_i):
                if getattr(prefs, f"submenu_{submenu_i.internal_name}_show"):
                    __menu_layout(layout,
                                  submenu_i,
                                  is_pie,
                                  as_buttons = getattr(prefs,
                                                       f"submenu_{submenu_i.internal_name}_buttons"),
                                  initial = True)
                else:  # If this menu is not shown, check if child submenus are renderable.
                    for submenu_c in submenu_i.children:
                        if issubclass(submenu_c, bpy.types.Menu):
                            if __menu_has_prefs(submenu_c):
                                if getattr(prefs, f"submenu_{submenu_c.internal_name}_show"):
                                    __menu_layout(layout,
                                                  submenu_c,
                                                  is_pie,
                                                  as_buttons = getattr(prefs,
                                                                       f"submenu_{submenu_c.internal_name}_buttons"),
                                                  initial = True)
                                    break
            else:
                __menu_layout(layout, submenu_i, is_pie)
                        
        except Exception as e:
            print(f"{ab_constants.error}Error displaying sub-menu. {e}")
    
    displayed_ops : int = 0
    for submenu_op in menu_ops:
        # Operator display
        if hasattr(submenu_op, "poll"):  # Does the operator have a "poll" function?
            if submenu_op.poll(context):
                layout.operator(submenu_op.bl_idname)
                displayed_ops += 1
            else:
                if is_pie:
                    box = layout.box()
                    box.label(text = submenu_op.bl_label)
                else:
                    layout.operator(submenu_op.bl_idname)
        else:
            layout.operator(submenu_op.bl_idname)
            displayed_ops += 1
    
    if len(menu_ops) > 0 and displayed_ops == 0:
        # box = layout.box()
        layout.label(text = ab_constants.missing_condition_msg)

class BaseMenu():
    bl_label = ab_constants.plugin_menu_name
    is_pie : bool

    @classmethod
    def change_bl_label(cls : type, text : str) -> None:
        """Changes the `bl_label` of the current class."""
        cls.text = text

class OBJECT_MT_ab_utility_base_menu(bpy.types.Menu, BaseMenu):
    """Main operator menu of the Blender Utility addon"""
    bl_idname = f"OBJECT_MT_{ab_constants.plugin_name_internal}_base_menu"
    is_pie = False
    children : list = []
    icon = None

    def draw(self, context):
        menu_draw(self, context)

class OBJECT_MT_ab_utility_base_menu_pie(bpy.types.Menu, BaseMenu):
    """Main pie operator menu of Blender Utility addon"""
    bl_idname = f"OBJECT_MT_{ab_constants.plugin_name_internal}_base_menu_pie"
    is_pie = True
    bl_label = ab_constants.plugin_menu_name + " Quick Menu"
    children : list = []
    icon = None

    def draw(self, context):
        menu_draw(self, context, is_pie = True)

__dynamic_menu_categories : set = set({})  # Variable used by dynamic submenu creation to keep track of the amount of menus generated.
__dynamic_menus : list = []

def __clear_vars() -> None:
    global __dynamic_menu_categories, __dynamic_menus
    __dynamic_menu_categories = set({})
    __dynamic_menus = []

def __does_dynamic_menu_exist(category : str = "Example/Category") -> bool:
    if category in __dynamic_menu_categories:
        return True
    return False

def create_dynamic_submenu_class(category : str = "Example/Category",
                                 classes : list = []) -> tuple[bpy.types.Menu]:
    global __dynamic_menu_categories, __dynamic_menus
    if category in __dynamic_menu_categories:
        return None
    category_split : list[str] = category.split("/")
    parent : str = "/".join(category_split[:1]) if len(category_split) > 1 else ""

    __dynamic_menu_categories.add(category)

    icon : str = 'COLLAPSEMENU'

    parent_menus : tuple[bpy.types.Menu] = None
    if not __does_dynamic_menu_exist(parent) and parent != "":
        parent_menus = create_dynamic_submenu_class(category = parent, classes = classes)
    menu_name : str = category_split[-1:][0]
    internal_name : str = menu_name.lower().replace(" ", "_").replace("/", "_")
    

    children : list[any] = []  # Operators and submenus that have the category value of the current menu.
    for cls in classes:
        if hasattr(cls, "category"):
            if cls.category == category:
                children.append(cls)
                if cls.category_icon != None:
                    icon = cls.category_icon

    children_pie : list[any] = children.copy()

    dynamic_cls = type(f"OBJECT_MT_{ab_constants.plugin_name_internal}_submenu_{internal_name}".format(),
                            (bpy.types.Menu,),
                            {

                                "bl_idname" : f"OBJECT_MT_{ab_constants.plugin_name_internal}_submenu_{internal_name}",
                                "bl_label" : menu_name,

                                "internal_name" : internal_name,
                                "parent" : parent,
                                "children" : children,
                                "category" : category,
                                "is_pie" : False,
                                "icon" : icon,

                                "draw" : lambda self, context: menu_draw(self, context, is_pie = False)
                            }
                         )

    dynamic_cls_pie = type(\
        f"OBJECT_MT_{ab_constants.plugin_name_internal}_submenu_{internal_name}_pie",
            (bpy.types.Menu,), 
            {
                "bl_idname" : f"OBJECT_MT_{ab_constants.plugin_name_internal}_submenu_{internal_name}_pie",
                "bl_label" : menu_name + " Pie Menu",

                "internal_name" : internal_name,
                "parent" : parent,
                "children" : children_pie,
                "category" : category,
                "is_pie" : True,
                "icon" : icon,

                "draw" : lambda self, context: menu_draw(self, context, is_pie = True)
            }
        )
    
    if dynamic_cls not in __dynamic_menus:
        __dynamic_menus.append(dynamic_cls)
    if dynamic_cls_pie not in __dynamic_menus:
        __dynamic_menus.append(dynamic_cls_pie)

    return (dynamic_cls, dynamic_cls_pie)

def menu_func(self : any, context : any) -> None:
    """This function is for the base operator menu in other menus."""
    layout = self.layout
    layout.separator()
    layout.menu(OBJECT_MT_ab_utility_base_menu.bl_idname)

# Base menu const ref
__menu : Final[tuple[bpy.types.Menu]] = (OBJECT_MT_ab_utility_base_menu,
                                         OBJECT_MT_ab_utility_base_menu_pie)

def __load(classes : list[bpy.types.Operator, bpy.types.Menu]) \
-> list[bpy.types.Menu]:
    global __init, __dynamic_menus
    if not __init:
        if classes is None:
            ValueError(f"{ab_constants.input_classes_none}")
        
        menus : list[bpy.types.Menu] = list(__menu)

        # Sorts classes by their "bl_idname"
        classes.sort(key = operator.attrgetter("bl_label"))
        
        # Filters classes in case there are other types.
        op_classes : list[bpy.types.Operator] = [op for op in classes if issubclass(op, bpy.types.Operator)\
                                                 and hasattr(op, "category")]
        
        # Unique menu set
        menu_set : set[bpy.types.Menu] = set({})

        # The menu structure is created here.
        for op_class in op_classes:
            # Example category = "Menu1/Menu2"
            if hasattr(op_class, "category"):
                menu_set.add(op_class.category)

        # dynamic_menus : list[tuple] = []
        for menu in menu_set:
            create_dynamic_submenu_class(category = menu, classes = op_classes)

        __dynamic_menus.sort(key = operator.attrgetter("bl_label"))

        for menu in menus:
            for submenu in __dynamic_menus:
                if submenu.parent == "" and\
                submenu.is_pie == False and\
                submenu not in menu.children:
                    menu.children.append(submenu)
            for op in op_classes:
                if op.category == "" and op not in menu.children:
                    menu.children.append(op)
            menu.children.sort(key = operator.attrgetter("bl_label"))

        # Parent menus
        for dynamic_menu in __dynamic_menus:
            for dynamic_menu2 in __dynamic_menus:
                if dynamic_menu != dynamic_menu2 and \
                dynamic_menu.category == dynamic_menu2.parent and \
                dynamic_menu2 not in dynamic_menu.children and \
                dynamic_menu.is_pie == dynamic_menu2.is_pie:
                    dynamic_menu.children.append(dynamic_menu2)
            dynamic_menu.children.sort(key = operator.attrgetter("bl_label"))

        menus += __dynamic_menus

        
        # Adds menus to different context menus
        bpy.types.VIEW3D_MT_object.append(menu_func)
        bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

        __init = True
        return menus
    else:
        RuntimeError(f"{ab_constants.menus_initialized}")

def load(classes : list[bpy.types.Operator | bpy.types.Panel | bpy.types.Panel]) \
-> list[bpy.types.Menu]:
    """Initializes operator menus.\n
    Returns a list of the newly generated menu classes."""
    if not __init:
        __clear_vars()
        menus : list[bpy.type.Menu] = []
        try:
            menus =  __load(classes)
        except Exception as e:
            print(f"{ab_constants.error}{e}")
        finally:
            return menus
    else:
        RuntimeError(f"{ab_constants.error}{ab_constants.menus_initialized}")

def unload() -> None:
    global __init
    if __init:
        __clear_vars()
        bpy.types.VIEW3D_MT_object.remove(menu_func)
        bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
        __init = False
    else:
        RuntimeError(f"{ab_constants.error}{ab_constants.menus_not_initialized}")