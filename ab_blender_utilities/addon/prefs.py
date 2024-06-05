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
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import AddonPreferences, PropertyGroup, UIList

import rna_keymap_ui
from . import constants, keymaps
from ..lib import fbx_files

class ABBU_PT_PrefTabs(PropertyGroup):
    tabs : EnumProperty(
        name = "Tabs",
        items=constants.e_pref_tab,
        default = 'PANELS'
    )

    menu_display_tabs : EnumProperty(
        name = "Tabs",
        items=constants.e_pref_display_tab,
        default = 'SUBMENUS'
    )

    quick_export_name_selection : IntProperty(
        description = "If a part of a child object's name is contained in this list,\nit will always be selected when exporting objects"
    )

class ABBU_PT_Quick_Export(PropertyGroup):
    arg_type : EnumProperty(
        name = "Type",
        items = constants.e_string_find_action,
        default = 'CONTAINS'
    )

class ABUTIL_UL_name_slots(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor = 0.3)
        split.prop(item, "name", icon = 'OBJECT_DATAMODE', emboss = False, text="")
        split.prop(item, "arg_type")

    def invoke(self, context, event):
        pass

class ABBU_AddonPreferences(AddonPreferences):
    bl_idname = __package__[:len(__package__)-6]

    panel_vars_ptr : PointerProperty(type=ABBU_PT_PrefTabs)

    # Utilities in properties
    utilties_in_properties : BoolProperty(
        name = "Utilities in the properties panel",
        default = False
    )

    # Quick export collection property
    quick_export_name_collection : CollectionProperty(
        type = ABBU_PT_Quick_Export
    )

    # Panel display

    show_cleanup_panel : BoolProperty(
        name = "Cleanup",
        default = True
    )

    show_data_panel : BoolProperty(
        name = "Data",
        default = True
   )

    show_file_panel : BoolProperty(
        name = "File",
        default = True
   )

    show_modifiers_panel : BoolProperty(
        name = "Modifiers",
        default = True
   )

    show_naming_panel : BoolProperty(
        name = "Naming",
        default = True
   )

    show_object_panel : BoolProperty(
        name = "Object",
        default = True
   )

    show_selection_panel : BoolProperty(
        name = "Selection",
        default = True
   )

    show_uv_panel : BoolProperty(
        name = "UVs",
        default = True
   )

    # Exporting

    uses_default_export_path : BoolProperty(
        name = "Use default export path",
        default = False
    )

    default_export_path : StringProperty(
        name = "Default Export Path",
        description = "Quick export directory path",
        subtype = 'DIR_PATH'
    )

    # Panels in properties
    show_object_attribute_utils_in_properties : BoolProperty(
        name = "Attribute Utilities in object properties",
        default = True
    )

    show_data_attribute_utils_in_properties : BoolProperty(
        name = "Attribute Utilities in data properties",
        default = True
    )

    show_color_attribute_utils_in_properties : BoolProperty(
        name = "Color Utilities in data properties",
        default = True
    )

    show_uv_attribute_utils_in_properties : BoolProperty(
        name = "UV Utilities in data properties",
        default = True
    )


    # Exporting

    fbx_exporter_type : EnumProperty(
        name = "Exporter Type",
        default = 'NATIVE',
        items = fbx_files.exporter_type
    )

    native_fbx_ex_check_existing : BoolProperty(
        name = "Check Existing",
        default = False,
        description = "When checked, prevents overwriting if the destination output file already exists."
    )

    native_fbx_ex_scale_options : EnumProperty(
        name = "Scale Option",
        items = fbx_files.scale_options,
        default = 'FBX_SCALE_CUSTOM',
        description = "The scale option for the FBX file.\n\
        It's recommended to use 'FBX_SCALE_CUSTOM' as that will export the scale as (1,1,1)"
    )

    native_fbx_ex_export_empty : BoolProperty(
        name = "Empty",
        default = True
    )

    native_fbx_ex_export_camera : BoolProperty(
        name = "Camera",
        default = False
    )

    native_fbx_ex_export_light : BoolProperty(
        name = "Light",
        default = False
    )

    native_fbx_ex_export_armature : BoolProperty(
        name = "Armature",
        default = True
    )

    native_fbx_ex_export_mesh : BoolProperty(
        name = "Mesh",
        default = True
    )

    native_fbx_ex_export_other : BoolProperty(
        name = "Other",
        default = False
    )

    native_fbx_ex_mesh_smooth_type : EnumProperty(
        name = "Mesh smooth type",
        items = fbx_files.mesh_smooth_types,
        default = 'OFF',
        description = "Mesh smoothing export.\n\
            Setting this to 'OFF' will export vertex normals.\n\
            Setting this to anything else will export either 'FACE' or 'EDGE' smoothing."
    )

    native_fbx_ex_use_tspace : BoolProperty(
        name = "Use Tangent Space",
        default = True,
        description = "Exports binormal and tangent vectors"
    )

    native_fbx_ex_use_custom_props : BoolProperty(
        name = "Export Custom Properties",
        default = True,
        description = "Exports custom properties"
    )

    do_not_load_keymaps : BoolProperty(
        name = "Do not load keymaps",
        default = False,
        description = "Prevents loading keymaps on start"
    )

    auto_re_add_missing_keymaps : BoolProperty(
        name = "Auto re-add missing keymaps",
        default = True,
        description = "Automatically adds in missing keymaps from the user keyconfig."
    )

    
    def draw(self, context) -> None:
        layout = self.layout
        column = layout.column(align=True)
        row = column.row()
        row.prop(self.panel_vars_ptr, "tabs", expand = True)

        box = column.box()

        if self.panel_vars_ptr.tabs == 'PANELS':
            self.__draw_panel_vis(box)
        elif self.panel_vars_ptr.tabs == 'KEYS':
            self.__draw_keymaps(box)
        elif self.panel_vars_ptr.tabs == 'QUICK_EXPORT':
            self.__draw_quick_export(box)
        elif self.panel_vars_ptr.tabs == 'ADVANCED':
            self.__draw_advanced(box)

    def __draw_quick_export_names(self, parent) -> None:

        row = parent.row()

        row.template_list("ABUTIL_UL_name_slots", "", self, "quick_export_name_collection", self.panel_vars_ptr, "quick_export_name_selection", rows=5)

        col = row.column(align=True)
        col.operator("object.abbu_add_remove_quick_export_names", icon='ADD', text="").arg = 'ADD'
        col.operator("object.abbu_add_remove_quick_export_names", icon='REMOVE', text="").arg = 'REMOVE'

    def __draw_panel_vis(self, parent) -> None:
        split = parent.split()
        box = split.box()
        box.label(text = "Visible Panels")
        box.prop(self, "show_cleanup_panel")
        box.prop(self, "show_data_panel")
        box.prop(self, "show_file_panel")
        box.prop(self, "show_modifiers_panel")
        box.prop(self, "show_naming_panel")
        box.prop(self, "show_object_panel")
        box.prop(self, "show_selection_panel")
        box.prop(self, "show_uv_panel")

    def __draw_keymaps(self, parent) -> None:
        split = parent.split()
        box = split.box()
        box.label(text = "Keymaps")

        column = box.column()
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        column.label(text = constants.prefs_keymap_do_not_remove_msg)
        column.label(text = constants.prefs_keymap_disable_msg)
        for km, kmi in keymaps.get_user_keymaps():
            if kmi is not None:
                km = km.active()
                column.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, column, 0)

        split = parent.split()
        box = split.box()
        column = box.column()
        column.prop(self, "do_not_load_keymaps")
        column.prop(self, "auto_re_add_missing_keymaps")

    def __draw_quick_export(self, parent) -> None:
        split = parent.split()
        column = split.column()
        box = column.box()
        box.prop(self, "fbx_exporter_type")
        box.prop(self, "uses_default_export_path")
        if self.uses_default_export_path:
            box.prop(self, "default_export_path")
        box.operator("wm.abbu_delete_quick_export_paths")
        box = column.box()
        if self.fbx_exporter_type == 'NATIVE':
            box.label(text = "Native FBX Export Preferences")
            box_naming = box.box()
            box_naming.label(text = "Quick Export Name Collection")
            box_naming.label(text = "Include the following objects despite their viewport display type:")
            self.__draw_quick_export_names(box_naming)
            box.prop(self, "native_fbx_ex_scale_options")
            box.prop(self, "native_fbx_ex_mesh_smooth_type")
            box.prop(self, "native_fbx_ex_use_tspace")
            box.prop(self, "native_fbx_ex_use_custom_props")
            row = box.column(align = True)
            row.prop(self, "native_fbx_ex_export_empty", icon = 'EMPTY_ARROWS')
            row.prop(self, "native_fbx_ex_export_camera", icon = 'CAMERA_DATA')
            row.prop(self, "native_fbx_ex_export_light", icon = 'LIGHT')
            row.prop(self, "native_fbx_ex_export_armature", icon = 'ARMATURE_DATA')
            row.prop(self, "native_fbx_ex_export_mesh", icon = 'MESH_DATA')
            row.prop(self, "native_fbx_ex_export_other", icon = 'FILE_3D')
            box.prop(self, "native_fbx_ex_check_existing")
        elif self.fbx_exporter_type == 'CUSTOM':
            box.label(text = "This is for custom exporters.")
