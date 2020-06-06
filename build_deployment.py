import os
from zipfile import ZipFile
import shutil

ls = os.listdir(".")

module_list = [
    name
    for name in ls
    if name
    not in ("test", "tests", ".mypy_cache", "bin", ".git", ".idea", "__pycache__")
    and os.path.isdir(os.path.join(".", name))
]

for module in module_list:
    shutil.make_archive(f"build\\{module}", "zip", module)

z = ZipFile("build/layer.zip", "a")
for name in ls:
    if (
        name.endswith((".py", ".json", ".sql", ".sqlite"))
        and not name.endswith("Template.py")
        and name != "build_deployment.py"
    ):
        z.write(name, f"/python/{name}")
z.close()
