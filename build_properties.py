BUILD_FOLDER = "build"
LAYER_NAME = "layer"
EXT_INCLUDE = (".py", ".json", ".sql", ".sqlite")
EXT_EXCLUDE = ("Template.py", "build_deployment.py", "build_properties.py")
LAMBDA_FUNCTION_DIRS = ["home", "item", "itembox", "match", "user"]
DIR_EXCLUDE = [
    "test",
    "tests",
    ".mypy_cache",
    "build",
    ".git",
    ".idea",
    "__pycache__",
]
