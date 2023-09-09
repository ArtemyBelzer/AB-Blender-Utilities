from . import ab_debug, ab_op_menus, ab_prefs

if not ab_debug.skip_loading_updater:
    from . import addon_updater
    from ..operators import addon_updater_ops

__init : bool = False

def __load_updater(bl_info : dict = None) -> None:
    addon_updater.Updater.addon = bl_info["name"]
    addon_updater.Updater.user = "ArtemyBelzer"
    addon_updater.Updater.repo = "AB-Blender-Utilities"
    addon_updater.Updater.current_version = bl_info["version"]
    addon_updater_ops.register(bl_info)
    addon_updater.Updater.check_for_update_now(callback=None)
        

def load(bl_info : dict) -> None:
    global __init
    __load_updater(bl_info)
    ab_prefs.UPDATE_UI = addon_updater_ops.update_settings_ui
    ab_op_menus.set_update_ui(addon_updater_ops.update_notice_box_ui)
    __init = True

def unload() -> None:
    global __init
    if __init:
        addon_updater_ops.unregister()
        ab_prefs.UPDATE_UI = None
        ab_op_menus.set_update_ui(None)
        __init = False