import os
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED

# region Set-up
from build_properties import (
    DIR_IGNORE,
    BUILD_FOLDER,
    EXT_INCLUDE,
    EXT_EXCLUDE,
    LAYER_NAME,
)

ls = os.listdir(".")
# endregion
# region Zip Lambda Functions
module_list = [
    name
    for name in ls
    if name not in DIR_IGNORE and os.path.isdir(os.path.join(".", name))
]
print(module_list)
for module in module_list:
    with ZipFile(f"{BUILD_FOLDER}/{module}.zip", "x", ZIP_STORED) as zf:
        for dirname, subdirs, files in os.walk(module):
            if dirname in DIR_IGNORE or any(
                DIR_IGNORE[i] in dirname for i in range(len(DIR_IGNORE))
            ):
                continue

            stripped_dir = dirname[len(module) + 1 :]
            if stripped_dir:
                zf.write(dirname, stripped_dir)
            for filename in files:
                zf.write(
                    os.path.join(dirname, filename),
                    os.path.join(stripped_dir, filename),
                )
# endregion
# region Zip Lambda Layer
layer_files = [
    name for name in ls if name.endswith(EXT_INCLUDE) and not name.endswith(EXT_EXCLUDE)
]
with ZipFile(
    f"{BUILD_FOLDER}/{LAYER_NAME}.zip", "x", ZIP_DEFLATED, compresslevel=9
) as z:
    all([z.write(name, f"/python/{name}")] for name in layer_files)
# endregion
