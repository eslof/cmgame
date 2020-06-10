from os import chdir
from typing import Dict, Literal, cast

from deployment_properties import PREFIX, DEFAULT_ZIP_DIR, DeployRoute
from deployment_ui import (
    input_zip_directory,
    input_action,
    input_zip_name,
    input_validate_new,
    input_name,
)
from deployment_utils import (
    publish_layer,
    update_function,
    create_function,
    get_list,
)

# region Set up
deployment_type = input_action(("function", "layer"), "Type to deploy")
directory = input_zip_directory(DEFAULT_ZIP_DIR)
chdir(directory)

print(f"\nPrinting list of current {deployment_type}s.")
lambda_data = get_list(deployment_type)
for entry in lambda_data:
    print(f"{entry} : {lambda_data[entry]}")

action = input_action(("new", "update"), "Action")
zip_name = input_zip_name()
default_name = f"{PREFIX}{zip_name}"
# endregion
# region Execution
route: Dict[str, DeployRoute] = {
    "function": {"update": update_function, "new": create_function},
    "layer": {"update": publish_layer, "new": publish_layer},
}
if action == "new":
    input_validate_new(lambda_data, zip_name, deployment_type)

lambda_name = input_name(lambda_data, default_name, deployment_type, action)

route[deployment_type][action](lambda_name, zip_name)
# endregion
