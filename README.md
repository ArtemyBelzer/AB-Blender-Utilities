# Artemy Belzer's Blender Utilities
## Note from Author
This plugin is a set of operators I have used throughout the years to speed up my workflow in Blender. These actions mainly organize and speed up content management in a DCC pipeline.

## Guide
### Accessing the main menu.
There are two ways to access the list of operators in the plugin.
By pressing `Alt+E` (default keymap).
By pressing `RMB/right-click` and navigating to the `Extra Utilities` submenu.
Go into the `Object` menu in the 3D viewport and navigate to the `Extra Utilities` submenu.

### Batch Rename+
![AB_Blender_Utilities_Batch_Rename_Plus_01](https://github.com/ArtemyBelzer/AB-Blender-Utilities/assets/143417950/b49bafc4-64c6-4f1a-b78e-a678049a3741)

The Batch Rename+ tool is based on the native Batch Rename tool by Blender. In addition to that it also has extended actions and some additional settings. You can open the Batch Rename+ tool by pressing `Ctrl+F2` (default keymap).
Native Batch Rename tool:
https://docs.blender.org/manual/en/latest/files/blend/rename.html#batch-rename
GitHub repo:
https://github.com/blender/blender/

#### Batch Rename+ Actions
- **Item Number:** 
The user can get the selected item number and either replace the name with the number or add it as a prefix/suffix.
-**Object Type:** 
The user can get the current object type and either replace the name with the type or add it as a prefix/suffix.
- **Splitter:** 
Adds a splitter to the name.
- **Active Object:** 
The user can get the current active object and either replace the name with the active object's name or add it as a prefix/suffix.
- **Utilities Expression:** 
Custom expression from AB Utilities. The syntax is from the old Auto/Advanced Rename tool.

![AB_Blender_Utilities_Batch_Rename_Plus_02](https://github.com/ArtemyBelzer/AB-Blender-Utilities/assets/143417950/ef46ed63-72a8-4232-b7e2-ec926a201f2e)

![AB_Blender_Utilities_Batch_Rename_Plus_03](https://github.com/ArtemyBelzer/AB-Blender-Utilities/assets/143417950/b02aa158-105f-4610-9db3-fc57a6e25fcd)


#### Batch Rename+ Advanced Settings
- Rename Data
Renames the object's data if it's present.
- Use custom numbering convention
Automatically numbers assets with the custom naming convention without manually specifying the action. If only one selected item is present, the numbering does not occur.
- Use a splitter between actions
Adds a splitter between every action that adds new content to the name.

#### Utilities Expression
The Utilities Expression action is context and argument-based. The Utilities Expression action rename your assets depending on the objects selected. When no argument is present, and multiple objects are selected, the operator renames the assets to "<New Name><Splitter><Count>". i.e. The third selected object in a selection of five after renaming will be "NewObjectName_03".

The user can supply the following expressions:
- **"$name"**: references the current name of the object.
- **"$type"**: returns the internal object type of an object. You can combine this with "$replace" to replace object types of Blender into some other naming convention. i.e. To rename "MESH" to "SM," use "$replace("MESH", "SM")".
- **"$active"**: returns the name of the currently active object in the scene.
- **"$index"**: returns the index of the currently selected object.
- **"$no_index"**: prevents the automatic addition of context-based numbering when renaming multiple objects.
- **"$replace(str_old, str_new)"**: finds all occurrences of the first argument and replaces them with the second one.

Usage example:
`$type$replace("MESH", "SM")_Cube`

![AB_Blender_Utilities_Auto_Advanced_Rename_Example](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/42a6cf37-e531-421e-83f1-baf1dbdb40ec)

### Alternative Menu layouts & Customization
Users can exclude specific categories from appearing in the plugin's "Quick Menu" (Alt+E). Submenu inclusion/exclusion can be found under the "General" tab in the plugin's properties; an alternative menu layout, a feature to draw operator menus as buttons, and a feature that adds certain utilities to the properties panel are also available.

![AB_Blender_Utilities_Alternative_Menu](https://github.com/ArtemyBelzer/AB-Blender-Utilities/assets/143417950/2df8adb4-52ce-4d3f-942f-8c8136a3d300)

![AB_Blender_Utilities_Menu_Customization](https://github.com/ArtemyBelzer/AB-Blender-Utilities/assets/143417950/346159ec-5c27-49bb-af45-4a7d2113ea40)

### Rebinding keys
![AB_Blender_Utilities_Preferences_Keymaps_Tab](https://github.com/ArtemyBelzer/AB-Blender-Utilities/assets/143417950/02b4e24d-4806-4ece-89e0-1ebb74bc18f2)
You can rebind keys inside Blender preferences by navigating to the plugin in the Add-ons tab. You can rebind the main menu, auto/advanced rename functionality, and the naming pie menu. If you would like to turn off the functioning of these keymaps, please uncheck the box on the left.

### Bulk Asset export
![AB_Blender_Utilities_Quick_Export](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/f51879e4-5c32-4a20-b7a7-e7ed898d0e77)

The user can select multiple assets in the scene and export them individually. This action also exports child assets. By default, the quick export action ignores assets rendered as a wireframe (viewport display as 'Wire'). You can export multiple selected assets or the currently active asset in the scene. The user can use directories in object names. During export, the quick export operators remove directories from the actual object name + data name.

#### Intermediate directory
To quickly export assets, you need an intermediate directory. To set an intermediate directory, set it by activating the "("Extra Utilities" or the Main Menu)/File/Set quick export path" operator.

Alternatively, the user can set a global, project-independent quick export directory in the "General" tab of the plugin preferences by checking "Use default export path".


Suppose the user wishes to remove any references to an intermediate directory in the project. In that case, the user can click the "Delete quick export attributes from scenes" in the "General" tab of the plugin preferences.

#### Quick Export Settings

The user can customize how the asset gets exported under the "Quick Export" tab of the plugin preferences. The user can pick the native FBX exporter or a custom implementation in the "Exporter Type" dropdown.

#### Quick Export Name Collection

The "Quick Export Name Collection" feature allows the user to export wired objects that begin, end, or have an occurrence of a string in their name. This name collection feature can be helpful when exporting collision objects with a mesh without having to tick "Export Wired" for quick exports. The "Quick Export Name Collection" feature is under the "Quick Export" tab in the addon properties.

## Bulk Attribute/Color/UV Operations
The plugin offers functionality to perform essential bulk attribute, colour, and UV operations on multiple objects. You can set the currently active UV map, rename a colour attribute on various objects, etc.

If the "Deselect Invalid" checkbox is present, the operator will deselect objects that do not contain the attribute post-operation.

![AB_Blender_Utilities_Delete_UV_Channel](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/184cd50e-5f3c-4233-a53c-206d569bfd96)

![AB_Blender_Utilities_Rename_UV_Channel](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/2ed05bb0-7acd-469b-ab28-4992690fb127)

![AB_Blender_Utilities_Set_Active_UV_Channel](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/67a9477a-9477-4192-b663-d7a343cca7af)

##  Clean up unused data blocks (Global Cleanup).
The "Global Cleanup" operator, under the "Cleanup" submenu, removes unused data blocks inside the current project file. The operator will delete any stored meshes/materials/textures/images with no references in the current project.

## Feature Overview
* Batch Rename+ with additional actions and functionality.
* Bulk UV utilities: Add, delete, rename, and set active functionality on multiple objects.
* Bulk Color Attribute/Vertex Color utilities: Delete, remove, rename, set to render, set active.
* Bulk asset quick export to an intermediate directory.
* Usage of directories in object names for quick exporting.
* Export/Import a point cloud of selected assets in a .JSON format for other applications.
* Cache object modifiers: create a non-evaluating copy of an object for quick previews.
* Select all objects referenced in modifiers.
* Remove unused materials on selected objects.
* Clean up unused data blocks (Global Cleanup).
* Reorder object data blocks alphabetically.
* Reorder modifier object data blocks to the modifier order.
* Store/Save the currently selected objects in Blender.
* Select all child objects recursively from the current parent.
* Randomize attributes on selected objects.
* Store the current object rotation as an attribute for retrieval later.
* Set attributes on selected objects.
* Append boolean operation to the name of boolean objects.
* Find and replace object names.
* Object names from parent.
* Set mesh data name from object name.
* Dynamically filled operator menu.

### Credits
This addon uses the Auto Updater from CGCookie.
https://github.com/CGCookie/blender-addon-updater

This addon uses code snippets from Blender
https://github.com/blender/blender
