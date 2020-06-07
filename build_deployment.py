import os
from zipfile import ZipFile
import shutil

# region Set-up
build_folder = "build"
layer_file_name = "layer"
ls = os.listdir(".")
layer_file_ext_include = (".py", ".json", ".sql", ".sqlite")
layer_file_ext_exclude = ("Template.py", "deployment.py")
folder_ignore = [
    "test",
    "tests",
    ".mypy_cache",
    "bin",
    ".git",
    ".idea",
    "__pycache__",
]
# endregion
# region Zip Lambda Functions
with [i for i in range(5)] as mylist:
    print(mylist[1])

with [
    name
    for name in ls
    if name not in folder_ignore and os.path.isdir(os.path.join(".", name))
] as module_list:
    for module in module_list:
        shutil.make_archive(f"{build_folder}\\{module}", "zip", module)
# endregion
# region Zip Lambda Layer
layer_files = [
    name
    for name in ls
    if name.endswith(layer_file_ext_include)
    and not name.endswith(layer_file_ext_exclude)
]
with ZipFile(f"{build_folder}/{layer_file_name}.zip", "a") as z:
    all([z.write(name, f"/python/{name}")] for name in layer_files)
# endregion
