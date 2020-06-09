BUILD_FOLDER = "bin"
LAYER_NAME = "layer"
EXT_INCLUDE = (".py", ".json", ".sql", ".sqlite")
EXT_EXCLUDE = ("Template.py", "build_deployment.py", "build_properties.py")
LAMBDA_FUNCTION_DIRS = ["home", "item", "itembox", "match", "user", "test"]
DIR_EXCLUDE = [
    "tests",
    "build",
    "deploy",
    "bin",
    ".mypy_cache",
    ".git",
    ".idea",
    "__pycache__",
]
