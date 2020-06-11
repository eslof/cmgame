from os import chdir

from deployment_properties import PREFIX, DEFAULT_ZIP_DIR, DeployRoute
import deployment_ui
import deployment_utils

# region Set up
deployment_type = deployment_ui.input_choice(("function", "layer"), "Type to deploy")
directory = deployment_ui.input_zip_directory(DEFAULT_ZIP_DIR)
chdir(directory)

lambda_data = deployment_utils.get_current(deployment_type)
if len(lambda_data) == 0:
    action = "new"
else:
    deployment_ui.print_lambda_data(lambda_data, f"available {deployment_type}s")
    action = deployment_ui.input_choice(("new", "update"), "Action")

zip_name = deployment_ui.input_zip_name()
default_name = f"{PREFIX}{zip_name}"
# endregion
# region Execution
if action == "new":
    deployment_ui.input_validate_new(lambda_data, zip_name, deployment_type)

route: DeployRoute = {
    "function": {
        "update": deployment_utils.update_function,
        "new": deployment_utils.create_function,
    },
    "layer": {
        "update": deployment_utils.publish_layer,
        "new": deployment_utils.publish_layer,
    },
}

lambda_name = deployment_ui.input_name(
    lambda_data, default_name, deployment_type, action
)
if deployment_type == "layer":
    route[deployment_type][action](lambda_name, zip_name)

elif deployment_type == "function":
    layers = deployment_utils.get_current("layer")
    if action == "new":
        function_layers = deployment_ui.input_layers_for_function_new(layers)
    elif action == "update":
        function_layers = deployment_ui.input_layers_for_function_update(
            lambda_name, layers
        )

    route[deployment_type][action](lambda_name, zip_name, function_layers)
# endregion
