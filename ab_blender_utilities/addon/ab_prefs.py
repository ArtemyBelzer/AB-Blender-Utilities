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
import rna_keymap_ui
from . import ab_constants, ab_keymaps
from ..lib import ab_fbx

class PanelVars(bpy.types.PropertyGroup):
    tabs : bpy.props.EnumProperty(
        name = "Tabs",
        items=ab_constants.e_pref_tab,
        default = 'GENERAL'
    )

class ABUtilAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__[:len(__package__)-6]

    panel_vars_ptr : bpy.props.PointerProperty(type=PanelVars)

    uses_default_export_path : bpy.props.BoolProperty(
        name = "Use default export path",
        default=False
    )

    default_export_path : bpy.props.StringProperty(
        name = "Default Export Path",
        description = "Quick export directory path",
        subtype = 'DIR_PATH'
    )

    name_splitter : bpy.props.StringProperty(
        name = "Name Splitter",
        default = "_",
        description = "Splitter that is used for auto naming.\n\
        Ex: \"ObjectName<splitter>01\", \
        \"ObjectName<splitter>02\""
    )

    name_padding : bpy.props.IntProperty(
        name = "Zero Padding Count",
        default = 1
    )

    # Exporting

    fbx_exporter_type : bpy.props.EnumProperty(
        name = "Exporter Type",
        default = 'NATIVE',
        items = ab_fbx.exporter_type
    )

    native_fbx_ex_check_existing : bpy.props.BoolProperty(
        name = "Check Existing",
        default = False,
        description = "When set to true, the FBX file will not export if it already exists"
    )

    native_fbx_ex_scale_options : bpy.props.EnumProperty(
        name = "Scale Option",
        items = ab_fbx.scale_options,
        default = 'FBX_SCALE_CUSTOM',
        description = "The scale option for the FBX file.\n\
        It's recommended to use 'FBX_SCALE_CUSTOM' as that will export the scale as (1,1,1)"
    )

    native_fbx_ex_export_empty : bpy.props.BoolProperty(
        name = "Empty",
        default = True
    )

    native_fbx_ex_export_camera : bpy.props.BoolProperty(
        name = "Camera",
        default = False
    )

    native_fbx_ex_export_light : bpy.props.BoolProperty(
        name = "Light",
        default = False
    )

    native_fbx_ex_export_armature : bpy.props.BoolProperty(
        name = "Armature",
        default = True
    )

    native_fbx_ex_export_mesh : bpy.props.BoolProperty(
        name = "Mesh",
        default = True
    )

    native_fbx_ex_export_other : bpy.props.BoolProperty(
        name = "Other",
        default = False
    )

    native_fbx_ex_mesh_smooth_type : bpy.props.EnumProperty(
        name = "Mesh smooth type",
        items = ab_fbx.mesh_smooth_types,
        default = 'OFF',
        description = "Mesh smoothing export.\n\
            Setting this to 'OFF' will export vertex normals.\n\
            Setting this to anything else will export either 'FACE' or 'EDGE' smoothing."
    )

    native_fbx_ex_use_tspace : bpy.props.BoolProperty(
        name = "Use Tangent Space",
        default = True,
        description = "Exports binormal and tangent vectors"
    )

    native_fbx_ex_use_custom_props : bpy.props.BoolProperty(
        name = "Export Custom Properties",
        default = True,
        description = "Exports custom properties"
    )

    do_not_load_keymaps : bpy.props.BoolProperty(
        name = "Do not load keymaps",
        default = False,
        description = "Prevents loading keymaps on start"
    )

    auto_re_add_missing_keymaps : bpy.props.BoolProperty(
        name = "Auto re-add missing keymaps",
        default = True,
        description = "Automatically adds in missing keymaps from the user keyconfig."
    )

    
    def draw(self, context) -> None:
        layout = self.layout  # bpy.types.UILayout 
        column = layout.column(align=True)
        row = column.row()
        row.prop(self.panel_vars_ptr, "tabs", expand=True)

        box = column.box()

        if self.panel_vars_ptr.tabs == 'GENERAL':
            self.draw_general(box)
        elif self.panel_vars_ptr.tabs == 'NAMING':
            self.draw_naming(box)
        elif self.panel_vars_ptr.tabs == 'KEYS':
            self.draw_keymaps(box)
        elif self.panel_vars_ptr.tabs == 'FBX EXPORTER':
            self.draw_fbx_export(box)
        elif self.panel_vars_ptr.tabs == 'ADVANCED':
            self.draw_advanced(box)

    def draw_advanced(self, parent) -> None:
        split = parent.split()
        box = split.box()
        box.label(text = "Advanced Menu")
        column = box.column()
        column.prop(self, "do_not_load_keymaps")
        column.label(text = self.bl_rna.properties["do_not_load_keymaps"].description)
        column.prop(self, "auto_re_add_missing_keymaps")
        column.label(text = self.bl_rna.properties["auto_re_add_missing_keymaps"].description)

    def draw_general(self, parent) -> None:
        split = parent.split()
        box = split.box()
        box.label(text = "General Preferences")
        box.prop(self, "uses_default_export_path")
        if self.uses_default_export_path:
            box.prop(self, "default_export_path")
        box.operator("wm.ab_delete_scene_quick_export_paths")

    def draw_naming(self, parent) -> None:
        split = parent.split()
        box = split.box()
        box.label(text = "Naming Preferences")
        box.prop(self, "name_splitter")
        box.prop(self, "name_padding")

    def draw_keymaps(self, parent) -> None:
        split = parent.split()
        box = split.box()
        box.label(text = "Keymaps")

        column = box.column()
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        column.label(text = ab_constants.prefs_keymap_do_not_remove_msg)
        column.label(text = ab_constants.prefs_keymap_disable_msg)
        for km, kmi in ab_keymaps.get_user_keymaps():
            if kmi is not None:
                km = km.active()
                column.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, column, 0)

    def draw_fbx_export(self, parent) -> None:
        split = parent.split()
        column = split.column()
        box = column.box()
        box.prop(self, "fbx_exporter_type")
        box = column.box()
        if self.fbx_exporter_type == 'NATIVE':
            box.label(text = "Native FBX Export Preferences")
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
            box.label(text = "A custom exporter can be implemented inside `operators\\file_ops\\file_ops_custom.py`.")
