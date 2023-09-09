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
import string
import re
from bl_operators import wm
from ..lib import ab_common, ab_naming_extra
from ..addon import ab_constants, ab_persistent
from bpy.app.translations import (
    pgettext_iface as iface_,
    pgettext_tip as tip_,
    contexts as i18n_contexts,
)


class CategoryNaming(ab_common.Category):
    """Operator category class for inheritance"""
    category = "Naming"
    category_arg = ab_common.OperatorCategories.SELECTION
    category_icon = 'GREASEPENCIL'

class OpABObjectNamesFromParent(bpy.types.Operator, CategoryNaming):
    """Renames child objects to match the naming of the parent object"""
    bl_idname = "wm.ab_object_names_from_parent"
    bl_label = "Object names from parent"
    bl_options = {'REGISTER', 'UNDO'}

    recursive : bpy.props.BoolProperty(
        name = "Recursive",
        default = True
    )

    rename_wireframe : bpy.props.BoolProperty(
        name = "Rename wireframe",
        default = True,
    )

    bake_alias_after_idx : bpy.props.BoolProperty(
        name = "Bake alias after index",
        default = True,
    )
    
    def execute(self, context):        
        for obj in bpy.context.selected_objects:
            # Selection
            obj_name_split : list = obj.name.split("/")
            obj_name : str = obj_name_split[len(obj_name_split)-1]
            obj_alias : str = ""
            if self.bake_alias_after_idx:
                for alias in ab_constants.bake_suffixes:
                    if alias in obj_name:
                        obj_alias = alias
                        obj_name = obj_name.replace(alias, "")
                        break
            ab_naming_extra.rename_child_objects(obj, obj_name, obj_alias, self.recursive, self.rename_wireframe)

        return {'FINISHED'}
    
class OpABUpdateMeshData(bpy.types.Operator, CategoryNaming):
    """Update mesh data name"""
    bl_idname = "wm.ab_update_mesh_data"
    bl_label = "Set mesh data name from object name"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if obj.data:
                obj.data.name = obj.name      
                        
        return {'FINISHED'}
    
# ABBatchRenameAction based on wm.BatchRenameAction from Blender
# GitHub Repo: https://github.com/blender/blender/
# Based on: https://github.com/blender/blender/blob/main/scripts/startup/bl_operators/wm.py
class ABBatchRenameAction(wm.BatchRenameAction):
    # category: StringProperty()
    type: bpy.props.EnumProperty(
        name="Operation",
        items=(
            ('REPLACE', "Find/Replace", "Replace text in the name"),
            ('SET', "Set Name", "Set a new name or prefix/suffix the existing one"),
            ('STRIP', "Strip Characters", "Strip leading/trailing text from the name"),
            ('CASE', "Change Case", "Change case of each name"),
            ('NUMBER', "Item Number", "The user can get the selected item number and either replace the name with the number or add it as a prefix/suffix."),
            ('TYPE', "Object Type", "The user can get the current object type and either replace the name with the type or add it as a prefix/suffix."),
            ('SPLITTER', "Splitter", "Adds a splitter to the name"),
            ('ACTIVE', "Active Object", "The user can get the current active object and either replace the name with the active object's name or add it as a prefix/suffix."),
            ('UTIL_EXPR', "Utilities Expression", "Custom expression from AB Utilities. The syntax is from the old Auto/Advanced Rename tool.")
        ),
        default = 'SET'
    )

    # type: 'SET'.
    set_name: bpy.props.StringProperty(name="Name")
    set_method: bpy.props.EnumProperty(
        name="Method",
        items=(
            ('NEW', "New", ""),
            ('PREFIX', "Prefix", ""),
            ('SUFFIX', "Suffix", "")
        ),
        default='NEW',
    )

# Batch Rename+ based on Batch Rename (wm.WM_OT_batch_rename) from Blender
# GitHub Repo: https://github.com/blender/blender/
# Based on: https://github.com/blender/blender/blob/main/scripts/startup/bl_operators/wm.py
class OpABBatchRenamePlus(wm.WM_OT_batch_rename, CategoryNaming):
    """Rename multiple items at once.\nThis operator includes extended functionality"""
    bl_idname = "wm.ab_batch_rename_plus"
    bl_label = "Batch Rename+"
    bl_options = {'REGISTER', 'UNDO'}

    # Old naming menu

    obj_name : bpy.props.StringProperty(
        name = "New Name",
        default = "",
    )

    obj_name_suffix : bpy.props.StringProperty(
        name = "Suffix",
        default = "",
    )

    obj_num_splitter : bpy.props.BoolProperty(
        name = "Split index",
        default = True
    )

    active_object_display : bpy.props.StringProperty(
        name = "Active Object",
        default = ""
    )

    auto_numbering : bpy.props.BoolProperty(
        name = "Auto numbering",
        default = False,
        description = "When checked, the Batch Rename+ tool will use a custom numbering convention (ie. \"_##\" vs the regular \".###\")."
    )

    name_splitter : bpy.props.StringProperty(
        name = "Name Splitter",
        default = "_",
        description = "Splitter that is used for auto naming.\n\
        Ex: \"ObjectName<splitter>01\", \
        \"ObjectName<splitter>02\""
    )

    use_unique_num_splitter : bpy.props.BoolProperty(
        name = "Unique Splitter",
        default = False
    )

    num_splitter : bpy.props.StringProperty(
        name = "Number Splitter",
        default = ".",
        description = "Splitter that is used for numbers."
    )

    num_padding : bpy.props.IntProperty(
        name = "Zero Padding Count",
        default = 1
    )

    default_loaded : bpy.props.BoolProperty(
        default = False
    )

    rename_data : bpy.props.BoolProperty(
        name = "Rename Data",
        default = True
    )

    use_a_splitter_between_actions : bpy.props.BoolProperty(
        name = "Use a splitter between actions",
        default = False,
        description = "Adds a splitter between batch naming actions"
    )

    actions: bpy.props.CollectionProperty(type=ABBatchRenameAction)

    adv_menu_state : bpy.props.BoolProperty(
        name = "Advanced Menu",
        default = False
    )

    def _add_splitter(self,
                      idx : int,
                      *,
                      is_number : bool = False) -> str:
        if self.use_a_splitter_between_actions:
            return self.num_splitter if is_number and self.use_unique_num_splitter else self.name_splitter
        return ""

    def _apply_actions(self,
                       actions : ABBatchRenameAction,
                       name : str,
                       idx : int,
                       item : bpy.types.Object,
                       item_count : int) -> str:
        for i, action in enumerate(actions):
            ty = action.type
            if ty == 'SET':
                text = action.set_name
                method = action.set_method
                if method == 'NEW':
                    name = text
                elif method == 'PREFIX':
                    name = text + self._add_splitter(i) + name
                elif method == 'SUFFIX':
                    name = name + self._add_splitter(i) + text
                else:
                    assert 0

            elif ty == 'STRIP':
                chars = action.strip_chars
                chars_strip = (
                    "%s%s%s"
                ) % (
                    string.punctuation if 'PUNCT' in chars else "",
                    string.digits if 'DIGIT' in chars else "",
                    " " if 'SPACE' in chars else "",
                )
                part = action.strip_part
                if 'START' in part:
                    name = name.lstrip(chars_strip)
                if 'END' in part:
                    name = name.rstrip(chars_strip)

            elif ty == 'REPLACE':
                if action.use_replace_regex_src:
                    replace_src = action.replace_src
                    if action.use_replace_regex_dst:
                        replace_dst = action.replace_dst
                    else:
                        replace_dst = action.replace_dst.replace("\\", "\\\\")
                else:
                    replace_src = re.escape(action.replace_src)
                    replace_dst = action.replace_dst.replace("\\", "\\\\")
                name = re.sub(
                    replace_src,
                    replace_dst,
                    name,
                    flags=(
                        0 if action.replace_match_case else
                        re.IGNORECASE
                    ),
                )
            elif ty == 'CASE':
                method = action.case_method
                if method == 'UPPER':
                    name = name.upper()
                elif method == 'LOWER':
                    name = name.lower()
                elif method == 'TITLE':
                    name = name.title()
                else:
                    assert 0
            elif ty == 'NUMBER':
                index_str = ab_common.pad_index(idx+1, self.num_padding)
                method = action.set_method
                if method == 'NEW':
                    name = index_str
                elif method == 'PREFIX':
                    name = item.type + self._add_splitter(i, is_number = True) + index_str
                elif method == 'SUFFIX':
                    name = index_str + self._add_splitter(i, is_number = True) + item.type
                else:
                    assert 0
            elif ty == 'TYPE':
                method = action.set_method
                if method == 'NEW':
                    name = item.type
                elif method == 'PREFIX':
                    name = item.type + self._add_splitter(i) + name
                elif method == 'SUFFIX':
                    name = name + self._add_splitter(i) + item.type
                else:
                    assert 0
            elif ty == 'SPLITTER':
                name += self.name_splitter
            elif ty == 'ACTIVE':
                active = bpy.context.active_object.name
                method = action.set_method
                if method == 'NEW':
                    name = active
                elif method == 'PREFIX':
                    name = active + self._add_splitter(i) + name
                elif method == 'SUFFIX':
                    name = name + self._add_splitter(i) + active
                else:
                    assert 0
            elif ty == 'UTIL_EXPR':
                text = action.set_name
                index_str : str = ab_common.pad_index(idx+1, self.num_padding)
                name = ab_naming_extra.object_name_variables(item, text, index_str)
            else:
                assert 0

        if self.auto_numbering and item_count > 1:
            index_str : str = ab_common.pad_index(idx+1, self.num_padding)
            name = name + self.num_splitter + index_str if self.use_unique_num_splitter else name + self.name_splitter + index_str
        return name

    def __old_execute(self, context):
        name_splitter = ""
        if self.obj_num_splitter:
            name_splitter = self.name_splitter
        
        for i, obj in enumerate(bpy.context.selected_objects):
            index_str : str = ab_common.pad_index(i+1, self.num_padding)
            object_name : str = ab_naming_extra.object_name_variables(obj, self.obj_name, index_str)
            obj.name = object_name if len(bpy.context.selected_objects) == 1\
                or "$no_index" in self.obj_name\
                or "$index" in self.obj_name\
                else object_name + name_splitter + index_str
            
            if self.obj_name_suffix != "":
               obj.name += ab_naming_extra.object_name_variables(obj, self.obj_name_suffix, index_str)
            
            if obj.data and self.rename_obj_data:
                obj.data.name = obj.name
            
        return {'FINISHED'}
    
    def _execute(self, context):
        seq, attr, descr = self._data

        actions = self.actions

        # Sanitize actions.
        for action in actions:
            if action.use_replace_regex_src:
                try:
                    re.compile(action.replace_src)
                except BaseException as ex:
                    self.report({'ERROR'}, "Invalid regular expression (find): " + str(ex))
                    return {'CANCELLED'}

                if action.use_replace_regex_dst:
                    try:
                        re.sub(action.replace_src, action.replace_dst, "")
                    except BaseException as ex:
                        self.report({'ERROR'}, "Invalid regular expression (replace): " + str(ex))
                        return {'CANCELLED'}

        total_len = 0
        change_len = 0
        for i, item in enumerate(seq):
            name_src = getattr(item, attr)
            name_dst = self._apply_actions(actions, name_src, i, item, len(seq))
            if name_src != name_dst:
                setattr(item, attr, name_dst)
                if self.rename_data:
                    if hasattr(item, "data"):
                        item.data.name = name_dst
                change_len += 1
            total_len += 1

        self.report({'INFO'}, tip_("Renamed %d of %d %s") % (change_len, total_len, descr))

        return {'FINISHED'}

    def execute(self, context):
        if not ab_persistent.get_preferences().legacy_rename_menu:
            return self._execute(context)
        else:
            return self.__old_execute(context)
    
    def invoke(self, context, event):
        self._data_update(context)

        if not self.actions:
            self.actions.add()
        if not self.default_loaded:
            prefs : bpy.types.AddonPreferences = ab_persistent.get_preferences()
            self.auto_numbering = prefs.auto_numbering
            self.num_padding = prefs.num_padding
            self.name_splitter = prefs.name_splitter
            self.use_a_splitter_between_actions = prefs.use_a_splitter_between_actions
            self.use_unique_num_splitter = prefs.use_unique_num_splitter
            self.num_splitter = prefs.num_splitter
            self.type = 'SET'
            self.default_loaded = True
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)
    
    def _advanced_menu(self, layout : bpy.types.UILayout) -> None:
        adv_menu_box = layout.box()
        row = adv_menu_box.row()
        row.prop(self,
                 "adv_menu_state",
                 icon = 'TRIA_DOWN' if self.adv_menu_state else 'TRIA_RIGHT',
                 icon_only = True,
                 emboss = False)
        row.label(text = "Advanced")

        if self.adv_menu_state:
            col = adv_menu_box.column()
            col.label(text = "Actions:")
            col.prop(self, "use_a_splitter_between_actions")
            col.separator()
            col.label(text = "Naming:")
            col.prop(self, "rename_data")
            col.prop(self, "name_splitter")
            col.separator()
            col.label(text = "Numbering:")
            col.prop(self, "auto_numbering")
            row = col.row()
            row.prop(self, "num_padding")
            row.prop(self, "use_unique_num_splitter")
            if self.use_unique_num_splitter:
                col.prop(self, "num_splitter")
    
    def __draw_old_menu(self, context) -> None:
        selected_objects : list[bpy.types.Object] = bpy.context.selected_objects
        active_object : bpy.types.Object = bpy.context.active_object

        layout = self.layout

        layout.prop(self, "obj_name")
        layout.prop(self, "obj_name_suffix")

        settings_box = layout.box()

        settings_box.prop(self, "rename_data")
        settings_box.prop(self, "obj_num_splitter")
        settings_box.prop(self, "padding")


        box = layout.box()
        object_count : int = len(selected_objects)
        object_suffix : str = "s" if object_count > 1 else ""

        box.label(text = f"{object_count} selected object{object_suffix}")
        # box.label(text = f"Active Object Name")
        self.active_object_display = active_object.name
        # box.prop(self, "active_object_display", emboss = False, text = "Active Object: ")
        box.label(text = f"Active Object: {active_object.name}")
        box.enabled = False

    

    def __draw_menu(self, context) -> None:
        """Menu akin to the one built into Blender"""
        layout = self.layout

        split = layout.split(align=True)
        split.row(align=True).prop(self, "data_source", expand=True)
        split.prop(self, "data_type", text="")

        for action in self.actions:
            box = layout.box()
            split = box.split(factor=0.87)

            # Column 1: main content.
            col = split.column()

            # Label's width.
            fac = 0.25

            # Row 1: type.
            row = col.split(factor=fac)
            row.alignment = 'RIGHT'
            row.label(text="Type")
            row.prop(action, "type", text="")

            ty = action.type
            if ty == 'SET':
                # Row 2: method.
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Method")
                row.row().prop(action, "set_method", expand=True)

                # Row 3: name.
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Name")
                row.prop(action, "set_name", text="")

            elif ty == 'STRIP':
                # Row 2: chars.
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Characters")
                row.row().prop(action, "strip_chars")

                # Row 3: part.
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Strip From")
                row.row().prop(action, "strip_part")

            elif ty == 'REPLACE':
                # Row 2: find.
                row = col.split(factor=fac)

                re_error_src = None
                if action.use_replace_regex_src:
                    try:
                        re.compile(action.replace_src)
                    except BaseException as ex:
                        re_error_src = str(ex)
                        row.alert = True

                row.alignment = 'RIGHT'
                row.label(text="Find")
                sub = row.row(align=True)
                sub.prop(action, "replace_src", text="")
                sub.prop(action, "use_replace_regex_src", text="", icon='SORTBYEXT')

                # Row.
                if re_error_src is not None:
                    row = col.split(factor=fac)
                    row.label(text="")
                    row.alert = True
                    row.label(text=re_error_src)

                # Row 3: replace.
                row = col.split(factor=fac)

                re_error_dst = None
                if action.use_replace_regex_src:
                    if action.use_replace_regex_dst:
                        if re_error_src is None:
                            try:
                                re.sub(action.replace_src, action.replace_dst, "")
                            except BaseException as ex:
                                re_error_dst = str(ex)
                                row.alert = True

                row.alignment = 'RIGHT'
                row.label(text="Replace")
                sub = row.row(align=True)
                sub.prop(action, "replace_dst", text="")
                subsub = sub.row(align=True)
                subsub.active = action.use_replace_regex_src
                subsub.prop(action, "use_replace_regex_dst", text="", icon='SORTBYEXT')

                # Row.
                if re_error_dst is not None:
                    row = col.split(factor=fac)
                    row.label(text="")
                    row.alert = True
                    row.label(text=re_error_dst)

                # Row 4: case.
                row = col.split(factor=fac)
                row.label(text="")
                row.prop(action, "replace_match_case")

            elif ty == 'CASE':
                # Row 2: method.
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Convert To")
                row.row().prop(action, "case_method", expand=True)

            elif ty == 'NUMBER':
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Method")
                row.row().prop(action, "set_method", expand=True)

            elif ty == 'TYPE':
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Method")
                row.row().prop(action, "set_method", expand=True)
            
            elif ty == 'ACTIVE':
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Method")
                row.row().prop(action, "set_method", expand=True)

            elif ty == 'UTIL_EXPR':
                row = col.split(factor=fac)
                row.alignment = 'RIGHT'
                row.label(text="Name")
                row.prop(action, "set_name", text="")

            # Column 2: add-remove.
            row = split.split(align=True)
            row.prop(action, "op_remove", text="", icon='REMOVE')
            row.prop(action, "op_add", text="", icon='ADD')

        layout.label(text=iface_("Rename %d %s") % (len(self._data[0]), self._data[2]), translate=False)
        layout = self.layout
        self._advanced_menu(layout)
        
    def draw(self, context):
        if not ab_persistent.get_preferences().legacy_rename_menu:
            self.__draw_menu(context)
        else:
            self.__draw_old_menu(context)
            

class OpABAppendBooleanOperationToName(bpy.types.Operator, ab_common.Category):
    """Reorders object data alphabetically.\nUseful for the FBX export order"""
    bl_idname = "wm.ab_append_boolean_operation_to_name"
    bl_label = "Append boolean operation to boolean object names"
    bl_options = {'REGISTER', 'UNDO'}

    category = "Naming"
    category_arg = ab_common.OperatorCategories.SELECTION

    prefix_length : bpy.props.IntProperty(
        name = "Prefix Length",
        default = 3
    )

    def execute(self, context):
        for obj in ab_common.get_selected_objects():
            for modifier in obj.modifiers:
                if hasattr(modifier, "object") and hasattr(modifier, "operation"):
                    if modifier.object:
                        modifier.object.name = f"{modifier.operation[:self.prefix_length]}_{modifier.object.name}"
        
        return {'FINISHED'}

PROPERTIES : tuple[bpy.types.PropertyGroup] = (ABBatchRenameAction,)
OPERATORS : tuple[bpy.types.Operator] = (OpABBatchRenamePlus,
                                         OpABObjectNamesFromParent,
                                         OpABUpdateMeshData,
                                         OpABAppendBooleanOperationToName)
