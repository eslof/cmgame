import os
from zipfile import ZipFile, ZIP_LZMA, ZIP_DEFLATED

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
    "build",
    ".git",
    ".idea",
    "__pycache__",
]
# endregion
# region Zip Lambda Functions
module_list = [
    name
    for name in ls
    if name not in folder_ignore and os.path.isdir(os.path.join(".", name))
]
print(module_list)
for module in module_list:
    with ZipFile(
        f"{build_folder}/{module}.zip", "x", ZIP_DEFLATED, compresslevel=9
    ) as zf:
        for dirname, subdirs, files in os.walk(module):
            if dirname in folder_ignore or "__pycache__" in dirname:
                continue

            stripped_dir = dirname[len(module) + 1 :]
            if stripped_dir:
                zf.write(dirname, stripped_dir)
            for filename in files:
                if "__pycache__" in filename:
                    continue
                print(filename)
                zf.write(
                    os.path.join(dirname, filename),
                    os.path.join(stripped_dir, filename),
                )
# endregion
# region Zip Lambda Layer
layer_files = [
    name
    for name in ls
    if name.endswith(layer_file_ext_include)
    and not name.endswith(layer_file_ext_exclude)
]
with ZipFile(
    f"{build_folder}/{layer_file_name}.zip", "x", ZIP_DEFLATED, compresslevel=9
) as z:
    all([z.write(name, f"/python/{name}")] for name in layer_files)
# endregion
