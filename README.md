This Blender addon is a collection of utilities designed to speed up your workflow. It includes features such as an FBX quick export button for exporting to an intermediate directory, batch UV and color attribute tools, and the ability to select all objects referenced in modifiers, among others.

The addon is built to allow new operators to be quickly added to its categorized panels and menus.

The Utilities menu can be accessed through the 3D Viewport panels, the addon's pie menu (default keymap `Alt + E`), the Object menu, or the Object context menu.

## Operators

### Cleanup

#### Data Blocks
- `Reorder Object Data Alphabetically`: Reorders object data blocks alphabetically.
- `Reorder Object Data Alphabetically Based On Modifiers`: Reorders object data blocks alphabetically based on the modifier order.

#### Materials
- `Remove Unused Materials`: Removes unused materials from the selected objects.

### Data

#### Color Attributes
- `Add Color Attribute`: Adds a color attribute to one or more selected objects.
- `Delete Color Attribute(s)`: Deletes the specified color attribute(s) from one or more selected objects.
- `Rename Color Attribute`: Renames the selected color attribute on one or more selected objects.
- `Set Active Color Attribute`: Sets the active color attribute on one or more selected objects.
- `Set Color Attributes To Render`: Specifies which color attribute should be rendered.

#### Custom Properties
- `Random Custom Property`: Randomizes a custom property on a selected object.
- `Set Custom Property`: Adds or sets a custom property.

### File

- `Set Quick Export Directory`: Opens a file browser to set the quick export directory.

#### FBX
- `Quick Export As FBX`: Exports one or more selected objects as FBX files, with an option to include child objects recursively.

#### Point Cloud
- `Export Point Cloud`: Exports the currently selected objects as a JSON file representing a point cloud.
- `Import Point Cloud`: Imports a JSON file containing a point cloud and creates instanced objects. An object must be selected before importing to instantiate from.

### Modifiers
- `Cache Modifiers`: Caches the modifiers of the currently selected object by duplicating it, applying modifiers on the duplicate, and hiding the original object with disabled modifiers.
- `Select Modifier Objects`: Selects the objects referenced inside modifiers on one or more objects.
- `Set Modifier Object(s) Viewport Visibility`: Sets the viewport visibility of objects referenced inside modifiers on one or more selected objects.
- `Uncache Modifiers`: Restores the original mesh with its modifiers prior to caching.

### Naming
- `Append Bool Operation To Bool Object Names`: Appends the boolean operation to the name of boolean objects. Select one or more objects that contain boolean modifiers.
- `Custom Expression Object Rename` (Default keymap `Alt + F2`): Renames one or more objects using custom expressions.
- `Object Names From Parent`: Renames child objects to match the naming of the parent object.
- `Update Data Name From Object Name`: Updates the data name (if present) of one or more selected objects to match the object name.

### Objects

#### Rotation
- `Restore Rotation`: Restores the rotation of one or more objects.
- `Store Rotation`: Stores the rotation of one or more objects.

### Selection
- `Select Child Objects`: Selects all child objects from the current object selection. This operator can select objects recursively.

#### Saving
- `Delete Saved Selection`: Deletes saved object selections created by the "Save Object Selection" operator.
- `Restore Object Selection`: Restores the saved object selections.
- `Save Object Selection`: Saves the currently selected objects. These selections can be restored using the "Restore Object Selection" operator.

### UVs
- `Add UV Layer`: Adds a UV layer to one or more objects.
- `Delete UV Layer(s)`: Deletes multiple UV layers from one or more objects. Any UV layers that are checked will be deleted.
- `Rename UV Layer`: Renames a UV layer on one or more objects.
- `Set Active UV Layer`: Sets the active UV layer on one or more objects.

## Custom Expression Object Rename

- `$name()`: Returns the current name of the object.
- `$type()`: Returns the object's type, e.g., MESH, CURVE, etc.
- `$active()`: Returns the name of the active object in Blender. Returns `None` if an active object is not present.
- `$idx()`: Returns the current index of the object.
- `$idx(<padding : int>)`: Returns the current index of the object with zero padding. The padding input should be an integer.
- `$oidx()`: Overrides the automatic index of the currently selected object. This works only when `Auto index on multiple` is checked in the operator.
- `$replace("<word1>", "<word2>")`: Replaces any instances of `word1` with `word2`.