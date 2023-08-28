# Artemy Belzer's Blender Utilities
### A plugin with additional utilities for speeding up workflow in Blender.
## Feature Overview
* Bulk asset quick export to an intermediate directory.
* Export/Import a point cloud of selected assets in a .JSON format for other applications.
* Cache object modifiers.
* Bulk UV utilities: Add, delete, rename, and set active functionality on multiple objects.
* Bulk Color Attribute/Vertex Color utilities: Delete, remove, rename, set to render, set active.
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
* Auto/Advanced rename with syntax and numbering conventions.
* Find and replace object names.
* Object names from parent.
* Set mesh data name from object name.
* Dynamically filled operator menu.

## Guide
### Accessing the main menu.
![AB_Blender_Utilities_Pie_Menu](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/38df762d-2cd9-4b83-ab76-1e430f692f64)

There are two ways to access the list of operators in the plugin.
By pressing Alt+E (default key binding).
By pressing right-click and navigating to the "Extra Utilities" submenu.
Go into the "Object" menu in the 3D viewport and navigate to the "Extra Utilities" submenu.
### Rebinding keys
![AB_Blender_Utilities_Keymaps](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/bc0a619f-e579-4dc3-8c90-44e80799894f)
You can rebind keys inside Blender preferences by navigating to the plugin in the Add-ons tab. You can rebind the main menu, auto/advanced rename functionality, and the naming pie menu. If you would like to turn off the functioning of these keymaps, please uncheck the box on the left.

### Bulk Asset export
![AB_Blender_Utilities_Quick_Export](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/f51879e4-5c32-4a20-b7a7-e7ed898d0e77)

The user can select multiple assets in the scene and export them individually. This action also exports child assets. By default, the quick export action ignores assets rendered as a wireframe (viewport display as 'Wire'). You can export multiple selected assets or the currently active asset in the scene.

#### Intermediate directory
To quickly export assets, you need an intermediate directory. To set an intermediate directory, set it by activating the "("Extra Utilities" or the Main Menu)/File/Set quick export path" operator.

Alternatively, the user can set a global, project-independent quick export directory in the "General" tab of the plugin preferences by checking "Use default export path".

![AB_Blender_Utilities_Preferences_General_Tab](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/e7b516d9-1b2c-483f-ad41-d8d411ed46c3)


Suppose the user wishes to remove any references to an intermediate directory in the project. In that case, the user can click the "Delete quick export attributes from scenes" in the "General" tab of the plugin preferences.

#### FBX Export Settings
![AB_Blender_Utilities_Preferences_FBX_Exporter_Tab](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/5634771b-307a-442f-bdab-63c88fd4b5dd)

The user can customize how the asset gets exported under the "FBX Exporter" tab of the plugin preferences. The user can pick the native FBX exporter or a custom implementation in the "Exporter Type" dropdown.

### Auto/Advanced Renaming
![AB_Blender_Utilities_Preferences_Naming_Tab](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/eef727c1-9652-4a7b-9fdf-054819aa72f9)

Users can set naming splitters and zero padding count under the plugin's "Naming" tab.

![AB_Blender_Utilities_Auto_Advanced_Rename](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/8c4ce9ac-6a94-47c7-b074-807e9d102261)

The auto-renaming utility is context and argument-based. The naming utility will rename your assets depending on the objects selected. When no argument is present, and multiple objects are selected, the operator renames the assets to "<New Name><Splitter><Count>". i.e. The third selected object in a selection of five after renaming will be "NewObjectName_03".
#### Arguments
The user can supply arguments to the naming utility.
"$name"
"$name" references the current name of the object.
"$type"
"$type" returns the internal object type of an object. You can combine this with "$replace" to replace object types of Blender into some other naming convention. i.e. To rename "MESH" to "SM," use "$replace("MESH", "SM")".
"$active"
"$active" returns the name of the currently active object in the scene.
"$index"
"$index" returns the index of the currently selected object.
"$no_index"
"$no_index" prevents the automatic addition of context-based numbering when renaming multiple objects.
"$replace(str_old, str_new)"
"$replace(str_old, str_new)" finds all occurrences of the first argument and replaces them with the second one.

Usage example:
`$type$replace("MESH", "SM")_Cube`

![AB_Blender_Utilities_Auto_Advanced_Rename_Example](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/42a6cf37-e531-421e-83f1-baf1dbdb40ec)


## Bulk Attribute/Color/UV Operations
The plugin offers functionality to perform essential bulk attribute, colour, and UV operations on multiple objects. You can set the currently active UV map, rename a colour attribute on various objects, etc.

If the "Deselect Invalid" checkbox is present, the operator will deselect objects that do not contain the attribute post-operation.
![AB_Blender_Utilities_Delete_UV_Channel](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/184cd50e-5f3c-4233-a53c-206d569bfd96)

![AB_Blender_Utilities_Rename_UV_Channel](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/2ed05bb0-7acd-469b-ab28-4992690fb127)

![AB_Blender_Utilities_Set_Active_UV_Channel](https://github.com/ArtemyBelzer/Artemy-Belzers-Blender-Utilities/assets/143417950/67a9477a-9477-4192-b663-d7a343cca7af)



##  Clean up unused data blocks (Global Cleanup).
The "Global Cleanup" operator, under the "Cleanup" submenu, removes unused data blocks inside the current project file. The operator will delete any stored meshes/materials/textures/images with no references in the current project.
