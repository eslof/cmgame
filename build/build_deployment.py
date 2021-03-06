import os
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED

# region Set-up
from build_properties import *

os.chdir("..")
ls = os.listdir(".")
# endregion
# region Zip Lambda Functions
for module in LAMBDA_FUNCTION_DIRS:
    with ZipFile(f"{BUILD_FOLDER}/{module}.zip", "x", ZIP_STORED) as zf:
        for dirname, subdirs, files in os.walk(module):
            if dirname in DIR_EXCLUDE:
                print(f"skipping {dirname}")
                continue

            stripped_dir = dirname[len(module) + 1 :]
            if stripped_dir:
                zf.write(dirname, stripped_dir)

            module_files = [
                name
                for name in files
                if name.endswith(EXT_INCLUDE) and not name.endswith(EXT_EXCLUDE)
            ]
            all(
                [
                    zf.write(
                        os.path.join(dirname, filename),
                        os.path.join(stripped_dir, filename),
                    )
                ]
                for filename in module_files
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
