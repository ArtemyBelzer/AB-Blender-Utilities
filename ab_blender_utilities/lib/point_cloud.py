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

import json
import collections


PointCloudPoint : type[tuple[any, ...]] = collections.namedtuple("PointCloudPoint", ["location", "rotation", "scale", "asset_path"])

def loads_json_data(json_data : str, present_key : str = "") -> dict | None:
    try:
        data_d : dict = json.loads(json_data)
        if present_key not in data_d and present_key != "":
            return None
        return data_d
    except Exception as e:
        print("Error parsing JSON file: " + e)
        return None

def parse_module_file_data(json_data : str = "") -> tuple | None:

    modules : tuple = tuple([m for m in loads_json_data(json_data, "modules")["modules"]])

    return modules

def dump_pc_data(data : list) -> str:
    """Returns point cloud data with JSON formatting"""
    point_cloud_d : dict = {"point_cloud" : []}
    for point in data:
        location : tuple(float) = getattr(point, "location")  # location
        rotation : tuple(float) = getattr(point, "rotation")  # rotation
        scale : tuple(float) = getattr(point, "scale")  # scale
        asset_path : str = getattr(point, "asset_path") if len(getattr(point, "asset_path")) < 4096 else ""  # asset path

        point_data_d : dict = {"location" : location,
                               "rotation" : rotation,
                               "scale" : scale,
                               "asset_path" : asset_path}
        
        point_cloud_d["point_cloud"].append(point_data_d)

    return json.dumps(point_cloud_d)

def load_pc_data(json_data : str) -> list | None:
    """Returns a list of points with original data for the points"""
    data : list = []  # Serialized data
    
    point_cloud_d : dict = json.loads(json_data)
    if "point_cloud" not in point_cloud_d:
        return None

    for point in point_cloud_d["point_cloud"]:
        location : tuple = tuple(point["location"])
        rotation : tuple = tuple(point["rotation"])
        scale : tuple = tuple(point["scale"])
        asset_path : str = point["asset_path"]
        
        data.append((location, rotation, scale, asset_path))
    
    return data
